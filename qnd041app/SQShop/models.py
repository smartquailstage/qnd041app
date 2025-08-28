from django.db import models

# Create your models here.
from django.db import models
from django.urls import reverse
from multiselectfield import MultiSelectField

class Category(models.Model):
    
    image = models.ImageField(upload_to='categories/%Y/%m/%d', blank=True, null=True)
    salidas = models.DateTimeField(null=True)
    desde = models.CharField(max_length=200, null=True)
    description = models.TextField(blank=True, null=True)
    detail = models.FileField(upload_to='tours/%Y/%m/%d', null=True)
    terms = models.TextField(blank=True, null=True)

        # Opciones de categoría
    CATEGORIA_CHOICES = [
        ('SaaS', 'Software como Servicio'),
        ('PaaS', 'Plataforma como Servicio'),
        ('IaaS', 'Infraestructura como Servicio'),
    ]

    SOFTWARE_CHOICES = [
        ('crm', 'SmartBusinessMedia - CRM'),
        ('erp', 'SmartBusinessAnalytics - ERP'),
    ]

    # Rangos de latencia
    LATENCIA_CHOICES = [
        ('500-800', 'Alta latencia (500–800 ms)'),
        ('300-500', 'Latencia elevada (300–500 ms)'),
        ('100-300', 'Latencia aceptable (100–300 ms)'),
        ('50-100',  'Baja latencia (50–100 ms)'),
        ('20-50',   'Muy baja latencia (20–50 ms)'),
        ('10-20',   'Latencia óptima (10–20 ms)'),
    ]

    # Rangos de usuarios simultáneos — alineados con latencia
    USUARIOS_SIMULTANEOS_CHOICES = [
        ('10-50', 'Baja concurrencia (10–50 usuarios)'),
        ('50-150', 'Carga ligera (50–150 usuarios)'),
        ('150-500', 'Carga media (150–500 usuarios)'),
        ('500-1000', 'Alta concurrencia (500–1000 usuarios)'),
        ('1000-5000', 'Carga crítica (1000–5000 usuarios)'),
        ('5000+', 'Alta disponibilidad (>5000 usuarios simultáneos)'),
    ]

    # Número de procesos
    NUMERO_PROCESOS_CHOICES = [
        ('5', '5 procesos'),
        ('10', '10 procesos'),
        ('20', '20 procesos'),
        ('40', '40 procesos'),
        ('80', '80 procesos'),
        ('100', '100 procesos'),
        ('200+', 'Más de 200 procesos'),
    ]

    PLATAFORMA_CHOICES = [
        ('ecommerce', 'Plataforma de Comercio Electrónico'),
        ('educacional', 'Plataforma Educativa Digital'),
        ('cadena_suministro', 'Sistema de Gestión de la Cadena de Suministro'),
        ('medico', 'Plataforma de Gestión Médica y Salud'),
        ('administracion_recursos', 'Plataforma de Administración de Recursos Empresariales'),
        ('gastronomia', 'Plataforma para Gestión de Recursos Gastronómicos'),
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

    nombre = models.CharField(max_length=4,null=True,blank=True, choices=CATEGORIA_CHOICES)
    slug = models.SlugField(max_length=200,null=True,blank=True, unique=True)
    software = MultiSelectField(choices=SOFTWARE_CHOICES, blank=True, null=True)
    plataforma = MultiSelectField(choices=PLATAFORMA_CHOICES, blank=True, null=True)
    numero_procesos = models.CharField(max_length=5, choices=NUMERO_PROCESOS_CHOICES,null=True,blank=True, default='5')
    automatizacion = MultiSelectField(choices=AUTOMATIZACION_CHOICES, blank=True, null=True)
    
    inteligencia_artificial = MultiSelectField(choices=IA_CHOICES, blank=True,null=True)
    latencia_aproximada = models.CharField(max_length=7,null=True,blank=True,choices=LATENCIA_CHOICES)
    usuarios_simultaneos = models.CharField(max_length=10,null=True,blank=True, choices=USUARIOS_SIMULTANEOS_CHOICES)

    def __str__(self):
        return f"{self.get_nombre_categoria_display()} - {self.numero_procesos} procesos"

    class Meta:
        verbose_name = 'Categoria de Producto'
        verbose_name_plural = 'Categorias de Productos'

    def __str__(self):
        return self.name or str(self.id)

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])





from decimal import Decimal, InvalidOperation
from django.db import models
from djmoney.models.fields import MoneyField
from djmoney.money import Money
from multiselectfield import MultiSelectField

class Product(models.Model):
    # Opciones
    SOFTWARE_CHOICES = [
        ('crm', 'SmartBusinessMedia - CRM'),
        ('erp', 'SmartBusinessAnalytics - ERP'),
    ]
    LATENCIA_CHOICES = [
        ('500-800', 'Alta latencia (500–800 ms)'),
        ('300-500', 'Latencia elevada (300–500 ms)'),
        ('100-300', 'Latencia aceptable (100–300 ms)'),
        ('50-100',  'Baja latencia (50–100 ms)'),
        ('20-50',   'Muy baja latencia (20–50 ms)'),
        ('10-20',   'Latencia óptima (10–20 ms)'),
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
    PLATAFORMA_CHOICES = [
        ('ecommerce', 'Plataforma de Comercio Electrónico'),
        ('educacional', 'Plataforma Educativa Digital'),
        ('cadena_suministro', 'Sistema de Gestión de la Cadena de Suministro'),
        ('medico', 'Plataforma de Gestión Médica y Salud'),
        ('administracion_recursos', 'Plataforma de Administración de Recursos Empresariales'),
        ('gastronomia', 'Plataforma para Gestión de Recursos Gastronómicos'),
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

    # Campos básicos
    name = models.CharField(max_length=200, db_index=True, null=True, blank=True)
    slug = models.SlugField(max_length=200, db_index=True, null=True, blank=True, unique=True)
    description = models.TextField(null=True, blank=True)
    price = MoneyField(max_digits=14, decimal_places=2, default_currency='USD', null=True, blank=True)
    category = models.ForeignKey('Category', related_name='products', on_delete=models.CASCADE, null=True, blank=True)
    available = models.BooleanField(default=True)
    iva = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="IVA (%)", null=True, blank=True)

    # Items
    item1 = models.CharField(max_length=200, null=True, blank=True)
    item2 = models.CharField(max_length=200, null=True, blank=True)
    item3 = models.CharField(max_length=200, null=True, blank=True)

    # Imágenes
    image = models.ImageField(upload_to='products/%Y/%m/%d', null=True, blank=True)
    image_2 = models.ImageField(upload_to='products/%Y/%m/%d', null=True, blank=True)
    image_3 = models.ImageField(upload_to='products/%Y/%m/%d', null=True, blank=True)

    # Tiempos
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    # Características técnicas
    software = MultiSelectField(choices=SOFTWARE_CHOICES, null=True, blank=True)
    plataforma = MultiSelectField(choices=PLATAFORMA_CHOICES, null=True, blank=True)
    numero_procesos = models.CharField(max_length=5, choices=NUMERO_PROCESOS_CHOICES, default='5', null=True, blank=True)
    automatizacion = MultiSelectField(choices=AUTOMATIZACION_CHOICES, null=True, blank=True)
    inteligencia_artificial = MultiSelectField(choices=IA_CHOICES, null=True, blank=True)
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

    # PaaS
    horas_desarrollo_paas = models.FloatField(verbose_name="Horas Desarrollo PaaS", null=True, blank=True)
    costo_hora_desarrollo_paas = MoneyField(max_digits=14, decimal_places=2, default_currency='USD', null=True, blank=True)
    costo_total_desarrollo_paas = MoneyField(max_digits=14, decimal_places=2, default_currency='USD', null=True, blank=True)

    horas_implementacion_paas = models.FloatField(verbose_name="Horas Implementación PaaS", null=True, blank=True)
    costo_hora_implementacion_paas = MoneyField(max_digits=14, decimal_places=2, default_currency='USD', null=True, blank=True)
    costo_total_implementacion_paas = MoneyField(max_digits=14, decimal_places=2, default_currency='USD', null=True, blank=True)

    margen_sq_paas = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    total_paas = MoneyField(max_digits=14, decimal_places=2, default_currency='USD', null=True, blank=True)
    total_paas_iva = MoneyField(max_digits=14, decimal_places=2, default_currency='USD', null=True, blank=True)

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

    # ▼ Helper seguro para MoneyField
    def _safe_money(self, val):
        try:
            return val if val else Money(0, 'USD')
        except (InvalidOperation, TypeError):
            return Money(0, 'USD')

    def save(self, *args, **kwargs):
        # Recalcula todos los totales
        # 1) Desarrollo
        costo_dev = Decimal(self.tiempo_desarrollo or 0) * self._safe_money(self.costo_hora_desarrollo).amount
        self.costo_total_desarrollo = Money(costo_dev, 'USD')

        costo_impl = Decimal(self.tiempo_implementacion or 0) * self._safe_money(self.costo_hora_implementacion).amount
        self.costo_project_management = Money(costo_impl, 'USD')

        margen_dev = costo_dev * Decimal('0.15')
        margen_impl = costo_impl * Decimal('0.10')
        self.margen_sq = round(margen_dev + margen_impl, 2)

        total_devimpl = costo_dev + costo_impl + Decimal(self.margen_sq or 0)
        self.total = Money(total_devimpl, 'USD')

        if self.iva is not None:
            iva_factor = Decimal(self.iva) / Decimal('100')
            self.total_iva = Money(total_devimpl * (1 + iva_factor), 'USD')
        else:
            self.total_iva = self.total

        # 2) PaaS
        costo_dev_paas = Decimal(self.horas_desarrollo_paas or 0) * self._safe_money(self.costo_hora_desarrollo_paas).amount
        self.costo_total_desarrollo_paas = Money(costo_dev_paas, 'USD')

        costo_impl_paas = Decimal(self.horas_implementacion_paas or 0) * self._safe_money(self.costo_hora_implementacion_paas).amount
        self.costo_total_implementacion_paas = Money(costo_impl_paas, 'USD')

        margen_paas = costo_dev_paas * Decimal('0.15') + costo_impl_paas * Decimal('0.10')
        self.margen_sq_paas = round(margen_paas, 2)

        total_paas_val = costo_dev_paas + costo_impl_paas + Decimal(self.margen_sq_paas or 0)
        self.total_paas = Money(total_paas_val, 'USD')

        if self.iva is not None:
            iva_factor = Decimal(self.iva) / Decimal('100')
            self.total_paas_iva = Money(total_paas_val * (1 + iva_factor), 'USD')
        else:
            self.total_paas_iva = self.total_paas

        # 3) Nube
        costo_nube = (
            self._safe_money(self.costo_cpu_mes).amount +
            self._safe_money(self.costo_bucket_mes).amount +
            self._safe_money(self.costo_balanceador_mes).amount
        )
        self.costo_total_nube = Money(costo_nube, 'USD')

        self.margen_sq_nube = round(costo_nube * Decimal('0.10'), 2)
        total_nube_val = costo_nube + Decimal(self.margen_sq_nube or 0)
        self.total_nube = Money(total_nube_val, 'USD')

        if self.iva is not None:
            iva_factor = Decimal(self.iva) / Decimal('100')
            self.total_nube_iva = Money(total_nube_val * (1 + iva_factor), 'USD')
        else:
            self.total_nube_iva = self.total_nube

        # 4) Arquitectura
        costo_arch = Decimal(self.tiempo_arquitectura or 0) * self._safe_money(self.costo_hora_arquitectura).amount
        costo_sre_val = self._safe_money(self.costo_sre).amount
        costo_arch_total = costo_arch + costo_sre_val

        self.margen_sq_arch = round(costo_arch_total * Decimal('0.10'), 2)
        total_arch_val = costo_arch_total + Decimal(self.margen_sq_arch or 0)
        self.total_arch = Money(total_arch_val, 'USD')

        if self.iva is not None:
            iva_factor = Decimal(self.iva) / Decimal('100')
            self.total_arch_iva = Money(total_arch_val * (1 + iva_factor), 'USD')
        else:
            self.total_arch_iva = self.total_arch

        # Finalmente, calcula price como suma de totales con IVA
        total_price_val = sum([
            self._safe_money(self.total_iva).amount,
            self._safe_money(self.total_paas_iva).amount,
            self._safe_money(self.total_nube_iva).amount,
            self._safe_money(self.total_arch_iva).amount,
        ], Decimal('0'))

        self.price = Money(total_price_val, 'USD')

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name or f"Product #{self.id}"








