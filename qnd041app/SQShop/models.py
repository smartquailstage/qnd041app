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
    numero_procesos = models.CharField(max_length=5, choices=NUMERO_PROCESOS_CHOICES,null=True,blank=True, default='5')
    automatizacion = MultiSelectField(choices=AUTOMATIZACION_CHOICES, blank=True, null=True)
    plataforma = MultiSelectField(choices=PLATAFORMA_CHOICES, blank=True, null=True)
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



from djmoney.models.fields import MoneyField

class Product(models.Model):

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
    name = models.CharField(max_length=200, db_index=True, null=True, blank=True)
    slug = models.SlugField(max_length=200, db_index=True, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    price = MoneyField(max_digits=14, decimal_places=2, default_currency='USD', null=True, blank=True)
    category = models.ForeignKey('Category', related_name='products', on_delete=models.CASCADE, null=True, blank=True)
    available = models.BooleanField(default=True, null=True, blank=True)
    iva = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Impuesto al valor agregado", null=True, blank=True)

    item1 = models.CharField(max_length=200, null=True, blank=True)
    item2 = models.CharField(max_length=200, null=True, blank=True)
    item3 = models.CharField(max_length=200, null=True, blank=True)

    image = models.ImageField(upload_to='products/%Y/%m/%d', null=True, blank=True)
    image_2 = models.ImageField(upload_to='products/%Y/%m/%d', null=True, blank=True)
    image_3 = models.ImageField(upload_to='products/%Y/%m/%d', null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    # Procesos y desarrollo
    numero_procesos = models.CharField(max_length=5, choices=NUMERO_PROCESOS_CHOICES,null=True,blank=True, default='5')
    tiempo_desarrollo = models.FloatField(verbose_name="Tiempo Desarrollo (D) en horas", null=True, blank=True)
    costo_hora_desarrollo = MoneyField(max_digits=14, decimal_places=2, default_currency='USD', null=True, blank=True, verbose_name="Costo/Hr Desarrollo (D)")
    costo_total_desarrollo = MoneyField(max_digits=14, decimal_places=2, default_currency='USD', null=True, blank=True, verbose_name="Costo Total Desarrollo (COSTO DEV)")

    tiempo_implementacion = models.FloatField(verbose_name="Tiempo Implementación (I) en horas", null=True, blank=True)
    costo_hora_implementacion = MoneyField(max_digits=14, decimal_places=2, default_currency='USD', null=True, blank=True, verbose_name="Costo/Hr Implementación (I)")
    costo_project_management = MoneyField(max_digits=14, decimal_places=2, default_currency='USD', null=True, blank=True, verbose_name="Costo de PM (COSTO PM)")

    margen_sq = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Margen SQ (%)", null=True, blank=True)
    total = MoneyField(max_digits=14, decimal_places=2, default_currency='USD', null=True, blank=True, verbose_name="Total sin IVA")
    total_iva = MoneyField(max_digits=14, decimal_places=2, default_currency='USD', null=True, blank=True, verbose_name="Total con IVA")

    # Servicios en la nube
    cloud_service_shared = models.CharField(max_length=100, verbose_name="Cloud Service Shared (Proveedor)", null=True, blank=True)
    latencia = models.CharField(max_length=50, verbose_name="Latencia Aproximada", null=True, blank=True)
    disponibilidad = models.CharField(max_length=100, verbose_name="Usuarios Simultáneos / Disponibilidad / Nodo", null=True, blank=True)
    vcpu = models.PositiveIntegerField(verbose_name="Cantidad de vCPU", null=True, blank=True)
    memoria_gb = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Memoria (GB)", null=True, blank=True)
    almacenamiento_gb = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Almacenamiento (GB)", null=True, blank=True)

    costo_cpu_mes = MoneyField(max_digits=14, decimal_places=2, default_currency='USD', null=True, blank=True, verbose_name="Costo/Mes por vCPU")
    costo_bucket_mes = MoneyField(max_digits=14, decimal_places=2, default_currency='USD', null=True, blank=True, verbose_name="Costo/Mes por Bucket")
    costo_balanceador_mes = MoneyField(max_digits=14, decimal_places=2, default_currency='USD', null=True, blank=True, verbose_name="Costo/Mes Balanceador de Carga")

    costo_total_nube = MoneyField(max_digits=14, decimal_places=2, default_currency='USD', null=True, blank=True, verbose_name="Costo Total en la Nube")
    margen_sq_nube = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Margen SQ Nube (%)", null=True, blank=True)
    total_nube = MoneyField(max_digits=14, decimal_places=2, default_currency='USD', null=True, blank=True, verbose_name="Total Nube sin IVA")
    total_nube_iva = MoneyField(max_digits=14, decimal_places=2, default_currency='USD', null=True, blank=True, verbose_name="Total Nube con IVA")

    # Arquitectura y SRE
    tipo_arquitectura = models.CharField(max_length=100, verbose_name="Tipo de Arquitectura", null=True, blank=True)
    tiempo_arquitectura = models.FloatField(verbose_name="Tiempo Arquitectura (horas)", null=True, blank=True)
    costo_hora_arquitectura = MoneyField(max_digits=14, decimal_places=2, default_currency='USD', null=True, blank=True, verbose_name="Costo/Hr Arquitectura")
    costo_sre = MoneyField(max_digits=14, decimal_places=2, default_currency='USD', null=True, blank=True, verbose_name="Costo SRE")
    margen_sq_arch = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Margen SQ Arquitectura (%)", null=True, blank=True)
    total_arch = MoneyField(max_digits=14, decimal_places=2, default_currency='USD', null=True, blank=True, verbose_name="Total Arquitectura sin IVA")
    total_arch_iva = MoneyField(max_digits=14, decimal_places=2, default_currency='USD', null=True, blank=True, verbose_name="Total Arquitectura con IVA")

    creado = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    actualizado = models.DateTimeField(auto_now=True, null=True, blank=True)

    def save(self, *args, **kwargs):

    if self.tiempo_desarrollo is not None and self.costo_hora_desarrollo:
        self.costo_total_desarrollo = Money(
            Decimal(str(self.tiempo_desarrollo)) * self.costo_hora_desarrollo.amount,
            'USD'
        )
    else:
        self.costo_total_desarrollo = Money(0, 'USD')

    if self.tiempo_implementacion is not None and self.costo_hora_implementacion:
        self.costo_project_management = Money(
            Decimal(str(self.tiempo_implementacion)) * self.costo_hora_implementacion.amount,
            'USD'
        )
    else:
        self.costo_project_management = Money(0, 'USD')

    # Calcular margen: 15% de desarrollo + 10% de implementación
    margen_dev = self.costo_total_desarrollo.amount * Decimal('0.15')
    margen_impl = self.costo_project_management.amount * Decimal('0.10')
    self.margen_sq = round(margen_dev + margen_impl, 2)

    # Total sin IVA
    self.total = Money(
        self.costo_total_desarrollo.amount + self.costo_project_management.amount + Decimal(str(self.margen_sq)),
        'USD'
    )

    # Total con IVA
    if self.iva is not None:
        iva_decimal = Decimal(str(self.iva)) / Decimal('100')
        self.total_iva = Money(
            self.total.amount + (self.total.amount * iva_decimal),
            'USD'
        )
    else:
        self.total_iva = self.total

    super().save(*args, **kwargs)

    def __str__(self):
        return f"Proceso #{self.id} - {self.numero_procesos or 'N/A'} procesos"

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])

    class Meta:
        verbose_name = "Costo por Proceso"
        verbose_name_plural = "Costos por Procesos"
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    








