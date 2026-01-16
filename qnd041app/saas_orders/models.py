from django.db import models
from saas_shop.models import Product
from decimal import Decimal
from django.core.validators import MinValueValidator, \
                                   MaxValueValidator
from saas_coupons.models import Coupon
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User, Group
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import RegexValidator
from decimal import Decimal
from djmoney.money import Money  # Asegúrate de importar si usas MoneyField
from djmoney.models.fields import MoneyField

# saas_orders/models.py
import hashlib
import uuid
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from django.db import models


class SaaSOrder(models.Model):
    SECTORES = [
        ('G', 'Gastronómico'),
        ('T', 'Turismo'),
        ('Th', 'Tecnología'),
        ('I', 'Industrial'),
        ('AG', 'Agricola'),
        ('I', 'Coorporativo'),
        ('E', 'Educativo'),
        ('A', 'Administrativo'),
        ('A', 'Finaciero'),
        ('M', 'Medico & Salud'),
        ('C', 'Contructivo'),
        ('Co', 'Comercial'),
        ('L', 'Legal'),
        ('ET', 'Entretenimiento'),
        ('M', 'Marketing & Publicitario'),
        ('GO', 'Gubernamental'),
        ('ONG', 'Organicion sin fines de lucro'),
        ('O', 'Otro'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='saas_orders',
        null=True,
        blank=True  
    )
    first_name = models.CharField(_('first name'), max_length=150, null=True, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, null=True, blank=True)
    email = models.EmailField(_('e-mail'),max_length=150, null=True, blank=True)
    ruc = models.CharField(_('R.U.C/C.I'), max_length=15,null=True, blank=True)
    razon_social = models.CharField(_('Razón Social'), max_length=200,null=True, blank=True)
    sector = models.CharField(_('Sector de Negocios'), max_length=100, choices=SECTORES,null=True, blank=True)
    phone_regex = RegexValidator(
        regex=r'^\+?593?\d{9,15}$',
        message="El número de teléfono debe estar en formato internacional. Ejemplo: +593XXXXXXXXX."
    )
    telefono = PhoneNumberField(
        verbose_name="Teléfono convencional de contacto",
        validators=[phone_regex],
        default='+593',
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False, verbose_name="Estado")
    force_paid = models.BooleanField(default=False, verbose_name="Forzar estado pagado")
    braintree_id = models.CharField(max_length=150, blank=True)
    coupon = models.ForeignKey(Coupon,
                               related_name='saas_orders',
                               null=True,
                               blank=True,
                               on_delete=models.SET_NULL)
    discount = models.IntegerField(default=0,
                                   validators=[MinValueValidator(0),
                                               MaxValueValidator(100)])

    # ------------------------------
    # Hashes por contrato
    # ------------------------------
    contract_hash_ip = models.CharField(max_length=64, unique=True, null=True, blank=True)
    contract_hash_dev = models.CharField(max_length=64, unique=True, null=True, blank=True)
    contract_hash_cloud = models.CharField(max_length=64, unique=True, null=True, blank=True)

    # ------------------------------
    # Firma IP
    # ------------------------------
    signed_contract_ip = models.FileField(upload_to='contracts/signed/', null=True, blank=True)
    contract_signed_at_ip = models.DateTimeField(null=True, blank=True)
    contract_verified_ip = models.BooleanField(default=False)

    # ------------------------------
    # Firma DEV
    # ------------------------------
    signed_contract_dev = models.FileField(upload_to='contracts/signed/', null=True, blank=True)
    contract_signed_at_dev = models.DateTimeField(null=True, blank=True)
    contract_verified_dev = models.BooleanField(default=False)

    # ------------------------------
    # Firma CLOUD
    # ------------------------------
    signed_contract_cloud = models.FileField(upload_to='contracts/signed/', null=True, blank=True)
    contract_signed_at_cloud = models.DateTimeField(null=True, blank=True)
    contract_verified_cloud = models.BooleanField(default=False)

    # Nuevos campos
    terms_accepted = models.BooleanField(default=False, verbose_name="Acepta términos y condiciones")
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    email_sent = models.BooleanField(default=False)  # nuevo campo para controlar envío de email

    # ==================================================
    # 🔐 HASH GENERATOR
    # ==================================================
    def _generate_contract_hash(self, contract_type: str) -> str:
        raw = (
            f"{self.id}|"
            f"{contract_type}|"
            f"{uuid.uuid4()}|"
            f"{timezone.now().isoformat()}|"
            f"{settings.SECRET_KEY}"
        )
        return hashlib.sha256(raw.encode()).hexdigest()

    def generate_contract_hash_ip(self):
        return self._generate_contract_hash("IP")

    def generate_contract_hash_dev(self):
        return self._generate_contract_hash("DEV")

    def generate_contract_hash_cloud(self):
        return self._generate_contract_hash("CLOUD")

    # ------------------------------

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Software As Service Order'
        verbose_name_plural = 'SaaS Orders'

    def __str__(self):
        return 'SaaS Order {}'.format(self.id)

    def get_total_cost(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        return total_cost - total_cost * (self.discount / Decimal('100'))
        

    def check_active_status(self):
        """Actualiza el estado a inactivo si han pasado más de 15 días desde la creación."""
        if self.is_active and self.created + timedelta(days=15) < timezone.now():
            self.is_active = False
            self.save()

    def save(self, *args, **kwargs):
        # ⚡ Detectar si force_paid cambia a True y aún no está marcado como pagado
        send_email = False
        if self.force_paid and not self.paid:
            self.paid = True
            if not self.email_sent:
                send_email = True  # marcar para enviar email después de guardar

        # Guardar cambios primero
        super().save(*args, **kwargs)

        # ⚡ Enviar correo con contratos generados automáticamente
        if send_email and self.email:
            domain = 'ec.smartquail.io'

            # Render HTML del correo
            html_message = render_to_string(
                'saas_orders/mails/invoices/payment_completed.html',
                {'order': self, 'domain': domain}
            )

            subject = f"Su pago se ha completado correctamente 🎉"
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = [self.email]

            email = EmailMultiAlternatives(
                subject,
                "Su pago ha sido registrado correctamente en nuestro sistema.",
                from_email,
                to_email
            )
            email.attach_alternative(html_message, "text/html")

            # ------------------------------
            # Generar los 3 contratos en PDF desde los templates
            # ------------------------------
            contracts_templates = [
                ('Contrato_IP.pdf', 'saas_orders/contracts/contract_ip.html', 'contract_hash_ip'),
                ('Contrato_DEV.pdf', 'saas_orders/contracts/contract_development.html', 'contract_hash_dev'),
                ('Contrato_CLOUD.pdf', 'saas_orders/contracts/contract_cloud_rent.html', 'contract_hash_cloud'),
            ]

            for filename, template, hash_field in contracts_templates:
                # Si el hash no existe, generar uno
                if not getattr(self, hash_field):
                    setattr(self, hash_field, getattr(self, f'generate_{hash_field}')())
                    super().save(update_fields=[hash_field])

                html_contract = render_to_string(
                    template,
                    {
                        'order': self,
                        'domain': domain,
                        'contract_hash': getattr(self, hash_field)
                    }
                )

                out = BytesIO()
                # Ajusta la ruta de tu CSS según tu proyecto
                css_path = f'saas_orders/static/css/{filename.lower().replace(".pdf","")}.css'
                weasyprint.HTML(string=html_contract, base_url=f"https://{domain}/").write_pdf(
                    out,
                    stylesheets=[weasyprint.CSS(css_path)],
                    presentational_hints=True
                )

                email.attach(filename, out.getvalue(), 'application/pdf')

            # ------------------------------
            # Enviar correo
            # ------------------------------
            try:
                email.send()
                self.email_sent = True
                super().save(update_fields=['email_sent'])
            except Exception as e:
                print(f"Error enviando email a {self.email}: {e}")

class SaaSOrderItem(models.Model):
    order = models.ForeignKey(SaaSOrder,
                              related_name='items',
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                related_name='saas_order_items',
                                on_delete=models.CASCADE)
    price = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = 'Software As Service Order'
        verbose_name_plural = 'SaaS Orders'

    def __str__(self):
        return f'{self.id}'

    def get_cost(self):
        return self.price * self.quantity

    # Rentabilidad por ítem
    @property
    def utilidad_bruta(self):
        return Decimal(self.product.utilidad_bruta.amount) if self.product.utilidad_bruta else Decimal('0.00')

    @property
    def valor_deducible_iva(self):
        return Decimal(self.product.valor_deducible_iva.amount) if self.product.valor_deducible_iva else Decimal('0.00')

    @property
    def utilidad_liquida(self):
        return Decimal(self.product.utilidad_liquida.amount) if self.product.utilidad_liquida else Decimal('0.00')




class Invoice(models.Model):
    number = models.CharField(max_length=20, unique=True)
    date_issued = models.DateTimeField(auto_now_add=True)
    customer_name = models.CharField(max_length=100)
    customer_ruc = models.CharField(max_length=13)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    iva = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    xml_signed = models.TextField(blank=True, null=True)  # XML firmado
    sri_status = models.CharField(max_length=50, default='pendiente')  # autorizado, rechazado, etc.
    access_key = models.CharField(max_length=49, unique=True)

    def __str__(self):
        return f"Factura {self.number}"
