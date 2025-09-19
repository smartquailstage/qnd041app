from django.db import models
from django.urls import reverse
from djmoney.models.fields import MoneyField
from djmoney.money import Money
from decimal import Decimal, InvalidOperation


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True, null=True, blank=True)
    
    slug = models.SlugField(max_length=200, db_index=True, unique=True, null=True, blank=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name or str(self.id)

    def get_absolute_url(self):
        return reverse('saas_shop:product_list_by_category', args=[self.slug])




class Product(models.Model):
    SOFTWARE_CHOICES = [
        ('Baja', 'disponibilidad Baja'),
        ('Mediana', 'disponibilidad Mediana'),
        ('Alta', 'disponibilidad Alta'),
        ('Muy Alta', 'disponibilidad Muy Alta'),
    ]
    LATENCIA_CHOICES = [
        ('500-800', 'Alta latencia (500–800 ms)'),
        ('300-500', 'Latencia elevada (300–500 ms)'),
        ('100-300', 'Latencia aceptable (100–300 ms)'),
        ('50-100', 'Baja latencia (50–100 ms)'),
        ('20-50', 'Muy baja latencia (20–50 ms)'),
        ('10-20', 'Latencia óptima (10–20 ms)'),
    ]
    USUARIOS_SIMULTANEOS_CHOICES = [
        ('10-50', 'Baja concurrencia (10–50 usuarios)'),
        ('50-150', 'Carga ligera (50–150 usuarios)'),
        ('150-500', 'Carga media (150–500 usuarios)'),
        ('500-1000', 'Alta concurrencia (500–1000 usuarios)'),
        ('1000-5000', 'Carga crítica (1000–5000 usuarios)'),
        ('5000+', 'Alta disponibilidad (>5000 usuarios simultáneos)'),
    ]
    NUMERO_PROCESOS_CHOICES = [
        ('5', '5 procesos'),
        ('10', '10 procesos'),
        ('20', '20 procesos'),
        ('40', '40 procesos'),
        ('80', '80 procesos'),
        ('100', '100 procesos'),
        ('200+', 'Más de 200 procesos'),
    ]
    AUTOMATIZACION_CHOICES = [
        ('chatbots', 'Automatización mediante Chatbots'),
        ('email_marketing', 'Envío Automático de Correos Electrónicos'),
        ('facturacion', 'Facturación Electrónica Automatizada'),
        ('crm_automatizado', 'Automatización de CRM (Gestión de Clientes)'),
        ('reserva_online', 'Gestión Automatizada de Reservas o Citas'),
        ('notificaciones', 'Notificaciones Automatizadas en Tiempo Real'),
        ('reportes', 'Generación Automática de Reportes'),
        ('seguimiento_clientes', 'Seguimiento Automático de Clientes'),
        ('procesamiento_pedidos', 'Automatización del Procesamiento de Pedidos'),
        ('sistemas_alertas', 'Sistemas de Alertas Automatizadas'),
    ]
    IA_CHOICES = [
        ('prediccion', 'Agente de IA de predicción'),
        ('segmentacion', 'Agente de IA de segmentación'),
        ('recomendacion', 'Agente de IA de recomendación'),
    ]

    name = models.CharField(max_length=200, db_index=True, null=True, blank=True)
    slug = models.SlugField(max_length=200, db_index=True, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    price = MoneyField(max_digits=14, decimal_places=2, default_currency='USD', null=True, blank=True)
    price_amount = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True, editable=False)

    category = models.ForeignKey('Category', related_name='products', on_delete=models.CASCADE, null=True, blank=True)
    available = models.BooleanField(default=True)
    iva = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="IVA (%)", null=True, blank=True)

    item1 = models.CharField(max_length=200, null=True, blank=True)
    item2 = models.CharField(max_length=200, null=True, blank=True)
    item3 = models.CharField(max_length=200, null=True, blank=True)

    image = models.ImageField(upload_to='products/%Y/%m/%d', null=True, blank=True)
    image_2 = models.ImageField(upload_to='products/%Y/%m/%d', null=True, blank=True)
    image_3 = models.ImageField(upload_to='products/%Y/%m/%d', null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    software = models.CharField(choices=SOFTWARE_CHOICES, null=True, blank=True,max_length=200)
    numero_procesos = models.CharField(max_length=5, choices=NUMERO_PROCESOS_CHOICES, default='5', null=True, blank=True)
    automatizacion = models.CharField(choices=AUTOMATIZACION_CHOICES, null=True, blank=True,max_length=200)
    inteligencia_artificial = models.CharField(choices=IA_CHOICES, null=True, blank=True,max_length=200)
    latencia_aproximada = models.CharField(max_length=7, choices=LATENCIA_CHOICES, null=True, blank=True)
    usuarios_simultaneos = models.CharField(max_length=10, choices=USUARIOS_SIMULTANEOS_CHOICES, null=True, blank=True)

    # Desarrollo
    tiempo_desarrollo = models.FloatField(verbose_name="Horas Desarrollo", null=True, blank=True)
    costo_hora_desarrollo = MoneyField(max_digits=14, decimal_places=2, default_currency='USD', null=True, blank=True)
    costo_total_desarrollo = MoneyField(max_digits=14, decimal_places=2, default_currency='USD', null=True, blank=True)

    tiempo_implementacion = models.FloatField(verbose_name="Horas Implementación", null=True, blank=True)
    costo_hora_implementacion = MoneyField(max_digits=14, decimal_places=2, default_currency='USD', null=True, blank=True)
    costo_project_management = MoneyField(max_digits=14, decimal_places=2, default_currency='USD', null=True, blank=True)

    margen_sq = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    total = MoneyField(max_digits=14, decimal_places=2, default_currency='USD', null=True, blank=True)
    total_iva = MoneyField(max_digits=14, decimal_places=2, default_currency='USD', null=True, blank=True)

    # Nube
    costo_cpu_mes = MoneyField(max_digits=14, decimal_places=2, default_currency='USD', null=True, blank=True)
    costo_bucket_mes = MoneyField(max_digits=14, decimal_places=2, default_currency='USD', null=True, blank=True)
    costo_balanceador_mes = MoneyField(max_digits=14, decimal_places=2, default_currency='USD', null=True, blank=True)

    costo_total_nube = MoneyField(max_digits=14, decimal_places=2, default_currency='USD', null=True, blank=True)
    margen_sq_nube = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    total_nube = MoneyField(max_digits=14, decimal_places=2, default_currency='USD', null=True, blank=True)
    total_nube_iva = MoneyField(max_digits=14, decimal_places=2, default_currency='USD', null=True, blank=True)

    # Arquitectura
    tiempo_arquitectura = models.FloatField(verbose_name="Horas Arquitectura", null=True, blank=True)
    costo_hora_arquitectura = MoneyField(max_digits=14, decimal_places=2, default_currency='USD', null=True, blank=True)
    costo_sre = MoneyField(max_digits=14, decimal_places=2, default_currency='USD', null=True, blank=True)

    margen_sq_arch = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    total_arch = MoneyField(max_digits=14, decimal_places=2, default_currency='USD', null=True, blank=True)
    total_arch_iva = MoneyField(max_digits=14, decimal_places=2, default_currency='USD', null=True, blank=True)

    # Nuevos campos
    utilidad_bruta = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True) 
    valor_deducible_iva = MoneyField(max_digits=14, decimal_places=2, default_currency='USD', null=True, blank=True)
    inversion_marketing = MoneyField(max_digits=14, decimal_places=2, default_currency='USD', null=True, blank=True)
    utilidad_liquida = MoneyField(max_digits=14, decimal_places=2, default_currency='USD', null=True, blank=True)


    def get_totals(self):
        """
        Calcula el subtotal (sin IVA), el valor del IVA y el total con IVA (price).
        Asume que `self.price` ya incluye IVA.
        """
        if not self.price or not self.price.amount:
            return {
                'subtotal': Decimal('0.00'),
                'iva_value': Decimal('0.00'),
                'total_with_iva': Decimal('0.00')
            }

        # Convertimos IVA a decimal (por ejemplo 16% → 0.16)
        iva_percentage = Decimal(self.iva or 0)
        iva_factor = iva_percentage / Decimal('100')

        # Subtotal = Precio total / (1 + IVA)
        subtotal = self.price.amount / (1 + iva_factor)

        # IVA = Precio total - Subtotal
        iva_value = self.price.amount - subtotal

        return {
            'subtotal': subtotal.quantize(Decimal('0.01')),
            'iva_value': iva_value.quantize(Decimal('0.01')),
            'total_with_iva': self.price.amount.quantize(Decimal('0.01'))
        }



    def _safe_money(self, val):
        try:
            return val if val else Money(0, 'USD')
        except (InvalidOperation, TypeError):
            return Money(0, 'USD')

    def save(self, *args, **kwargs):
        # 1) Desarrollo e implementación
        costo_dev = Decimal(self.tiempo_desarrollo or 0) * self._safe_money(self.costo_hora_desarrollo).amount
        self.costo_total_desarrollo = Money(costo_dev, 'USD')

        costo_impl = Decimal(self.tiempo_implementacion or 0) * self._safe_money(self.costo_hora_implementacion).amount
        self.costo_project_management = Money(costo_impl, 'USD')

        margen_dev = costo_dev * Decimal('0.15')
        margen_impl = costo_impl * Decimal('0.10')
        self.margen_sq = round(margen_dev + margen_impl, 2)

        total_devimpl = costo_dev + costo_impl + Decimal(self.margen_sq or 0)
        self.total = Money(total_devimpl, 'USD')

        iva_factor = Decimal(self.iva or 0) / Decimal('100')
        self.total_iva = Money(total_devimpl * (1 + iva_factor), 'USD')

        # 2) Nube
        costo_nube = (
            self._safe_money(self.costo_cpu_mes).amount +
            self._safe_money(self.costo_bucket_mes).amount +
            self._safe_money(self.costo_balanceador_mes).amount
        )
        self.costo_total_nube = Money(costo_nube, 'USD')
        self.margen_sq_nube = round(costo_nube * Decimal('0.20'), 2)
        total_nube_val = costo_nube + Decimal(self.margen_sq_nube or 0)
        self.total_nube = Money(total_nube_val, 'USD')
        self.total_nube_iva = Money(total_nube_val * (1 + iva_factor), 'USD')

        # 3) Arquitectura
        costo_arch = Decimal(self.tiempo_arquitectura or 0) * self._safe_money(self.costo_hora_arquitectura).amount
        costo_sre_val = self._safe_money(self.costo_sre).amount
        costo_arch_total = costo_arch + costo_sre_val

        self.margen_sq_arch = round(costo_arch_total * Decimal('0.10'), 2)
        total_arch_val = costo_arch_total + Decimal(self.margen_sq_arch or 0)
        self.total_arch = Money(total_arch_val, 'USD')
        self.total_arch_iva = Money(total_arch_val * (1 + iva_factor), 'USD')

        # 4) Precio final
        total_price_val = sum([
            self._safe_money(self.total_iva).amount,
            self._safe_money(self.total_nube_iva).amount,
            self._safe_money(self.total_arch_iva).amount,
        ], Decimal('0'))
        self.price = Money(total_price_val, 'USD')

        # 5) Utilidad Bruta (suma de márgenes)
        total_margen = Decimal(self.margen_sq or 0) + Decimal(self.margen_sq_nube or 0) + Decimal(self.margen_sq_arch or 0)
        self.utilidad_bruta = total_margen

        # 6) Valor deducible de impuestos (total_iva - 15%)
        iva_deducible = self._safe_money(self.total_iva).amount * Decimal('0.85')
        self.valor_deducible_iva = Money(iva_deducible, 'USD')

        # 7) Utilidad líquida = utilidad_bruta - inversion_marketing
        utilidad_liquida_val = total_margen - self._safe_money(self.inversion_marketing).amount
        self.utilidad_liquida = Money(utilidad_liquida_val, 'USD')

        self.price_amount = self.price.amount if self.price else None


        super().save(*args, **kwargs)

    def __str__(self):
        return self.name or f"Product #{self.id}"

    def get_absolute_url(self):
        return reverse('saas_shop:product_detail', args=[self.id, self.slug])
