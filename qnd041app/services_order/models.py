from django.db import models
from saas_shop.models import Product
from decimal import Decimal
from django.core.validators import MinValueValidator, \
                                   MaxValueValidator
from services_coupons.models import Coupon
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User, Group
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import RegexValidator
from decimal import Decimal
from djmoney.money import Money  # Asegúrate de importar si usas MoneyField
from djmoney.models.fields import MoneyField

class ServicesOrder(models.Model):
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
    regex=r'^\d{9}$',
    message="Ingrese solo los 9 dígitos del número de teléfono, sin el prefijo +593."
    )

    telefono = models.CharField(validators=[phone_regex], max_length=9)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False, verbose_name="Estado")
    braintree_id = models.CharField(max_length=150, blank=True)
    coupon = models.ForeignKey(Coupon,
                               related_name='saas_orders',
                               null=True,
                               blank=True,
                               on_delete=models.SET_NULL)
    discount = models.IntegerField(default=0,
                                   validators=[MinValueValidator(0),
                                               MaxValueValidator(100)])

    
    # Nuevos campos
    terms_accepted = models.BooleanField(default=False, verbose_name="Acepta términos y condiciones")
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    email_sent = models.BooleanField(default=False)  # nuevo campo para controlar envío de email

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




class ServicesOrderItem(models.Model):
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
