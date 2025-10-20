from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from usuarios.models  import SmartQuailCrew
from saas_shop.models import Product



class BusinessSystemProject(models.Model):
    # Campo para el usuario logueado (asociado con el modelo de usuario)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='business_projects',
        verbose_name='Producto asociado'
    )

    # Nombre y descripción del proyecto
    name = models.CharField(max_length=200)
    description = models.TextField()

    # Fecha de creación
    created_at = models.DateTimeField(auto_now_add=True)

    # ✅ Relación con el equipo de SmartQuail
    crew_members = models.ManyToManyField(
        'usuarios.SmartQuailCrew',
        related_name='projects',
        blank=True,
        verbose_name='Equipo asignado'
    )

    # Nuevo campo: Sector de negocio (con opciones predefinidas)
    SECTOR_CHOICES = [
        ('gastronomico', 'Gastronómico'),
        ('servicios', 'Servicios'),
        ('administrativo', 'Administrativo'),
        ('finanzas', 'Finanzas'),
        ('banca', 'Banca'),
        ('gubernamental', 'Organización Gubernamental'),
        ('no_gubernamental', 'No Gubernamental'),
        ('comercio_electronico', 'Comercio Electrónico'),
        ('marketing_publicidad', 'Marketing y Publicidad'),
        ('educativo', 'Educativo'),
        ('medico_salud', 'Médico y Salud'),
        ('transporte', 'Transporte'),
        ('cadena_suministros', 'Cadena de Suministros'),
        ('agricultura', 'Agricultura'),
    ]

    business_sector = models.CharField(
        max_length=50,
        choices=SECTOR_CHOICES,
        default='gastronomico',  # O puedes dejarlo en blanco
        verbose_name='Sector de Negocio'
    )


    def __str__(self):
        return self.name



    def get_absolute_url(self):
        return reverse("business:project_detail", kwargs={"pk": self.pk})

from usuarios.models import SmartQuailCrew  # Asegúrate de que esta importación es correcta

from django.db import models
from usuarios.models import SmartQuailCrew
from datetime import date

class BusinessProcess(models.Model):
    project = models.ForeignKey(
        'BusinessSystemProject',
        on_delete=models.CASCADE,
        related_name='processes'
    )
    name = models.CharField(max_length=200)
    description = models.TextField()

    progress = models.IntegerField(help_text="Progreso del 0 al 100 (%)")

    has_automation = models.BooleanField(default=False)
    automation_description = models.TextField(blank=True, null=True)

    has_ai = models.BooleanField(default=False)
    ai_model_description = models.TextField(
        blank=True, null=True,
        help_text="Describe el modelo de IA y su implementación en el proceso"
    )

    # 👤 Desarrollador asignado
    assigned_developer = models.ForeignKey(
        SmartQuailCrew,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_processes',
        verbose_name="Desarrollador asignado"
    )

    # 📅 Nuevas fechas
    start_date = models.DateField("Fecha de inicio", null=True, blank=True)
    delivery_date = models.DateField("Fecha de entrega", null=True, blank=True)

    approved_by_client = models.BooleanField("¿Aprobado por cliente?", default=False)

    PROCESS_TYPE_CHOICES = [
        ('I', 'Investigación'),
        ('D', 'Desarrollo'),
    ]
    process_type = models.CharField(
        "Tipo de proceso",
        max_length=1,
        choices=PROCESS_TYPE_CHOICES,
        blank=True,
        null=True
    )

    TECHNOLOGY_TYPE_CHOICES = [
    ('frontend', 'Frontend'),
    ('backend', 'Backend'),
    ]
    
    technology_type = models.CharField(
    "Tipo de Tecnología",
    max_length=10,
    choices=TECHNOLOGY_TYPE_CHOICES,
    blank=True,
    null=True,
    )


    PROCESS_CLASS_CHOICES = [
        ('interview', 'Entrevistas'),
        ('erp_impl', 'Implementación SmartBusinessAnalytics®-ERP'),
        ('crm_impl', 'Implementación SmartBusinessMedia®-CRM'),
        ('uiux_dev', 'Desarrollo Interfase UI/UX'),
        ('architecture_dev', 'Desarrollo de Arquitectura'),
    ]
    process_class = models.CharField(
        "Clase del proceso",
        max_length=30,
        choices=PROCESS_CLASS_CHOICES,
        blank=True,
        null=True
    )

    final_url = models.URLField("URL final", blank=True, null=True)


    # 🕓 Cálculo de duración
    total_development_days = models.PositiveIntegerField(
        "Días de desarrollo", null=True, blank=True, editable=False
    )

    def save(self, *args, **kwargs):
        if self.start_date and self.delivery_date:
            delta = self.delivery_date - self.start_date
            self.total_development_days = delta.days if delta.days >= 0 else 0
        else:
            self.total_development_days = None
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.project.name}"





class BusinessAutomation(models.Model):
    project = models.ForeignKey(
        'BusinessSystemProject',
        on_delete=models.CASCADE,
        related_name='automations'
    )
    
    name = models.CharField(max_length=200)
    description = models.TextField()

    progress = models.IntegerField(help_text="Progreso del 0 al 100 (%)")

    # Tipos de automatización
    AUTOMATION_TYPE_CHOICES = [
        ('email', 'Email'),
        ('auto_auth', 'Autoidentificación'),
        ('report_gen', 'Generación de reportes'),
        ('chatbot', 'Chatbot para negocios'),
        ('data_sync', 'Sincronización de datos'),
        ('notification', 'Notificaciones automáticas'),
        ('workflow', 'Automatización de flujos de trabajo'),
    ]
    automation_type = models.CharField(
        "Tipo de automatización",
        max_length=20,
        choices=AUTOMATION_TYPE_CHOICES,
        blank=True,
        null=True
    )

    # 👤 Desarrollador asignado
    assigned_developer = models.ForeignKey(
        SmartQuailCrew,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_automations',
        verbose_name="Desarrollador asignado"
    )

    # 📅 Fechas
    start_date = models.DateField("Fecha de inicio", null=True, blank=True)
    delivery_date = models.DateField("Fecha de entrega", null=True, blank=True)

    approved_by_client = models.BooleanField("¿Aprobado por cliente?", default=False)

    final_url = models.URLField("URL final", blank=True, null=True)

    # 🕓 Cálculo de duración
    total_development_days = models.PositiveIntegerField(
        "Días de desarrollo", null=True, blank=True, editable=False
    )

    def save(self, *args, **kwargs):
        if self.start_date and self.delivery_date:
            delta = self.delivery_date - self.start_date
            self.total_development_days = delta.days if delta.days >= 0 else 0
        else:
            self.total_development_days = None
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.project.name}"



from datetime import date

class BusinessIntelligent(models.Model):
    project = models.ForeignKey(
        'BusinessSystemProject',
        on_delete=models.CASCADE,
        related_name='intelligents'
    )
    name = models.CharField(max_length=200)
    description = models.TextField()

    progress = models.IntegerField(help_text="Progreso del 0 al 100 (%)")

    # Tipos de inteligencia artificial
    AI_TYPE_CHOICES = [
        ('binary_classification', 'Predicción por clasificación binaria'),
        ('regression', 'Predicción por regresión'),
        ('clustering', 'Clustering'),
        ('nlp', 'Procesamiento de Lenguaje Natural (NLP)'),
        ('image_recognition', 'Reconocimiento de imágenes'),
        ('recommendation', 'Sistemas de recomendación'),
        ('reinforcement_learning', 'Aprendizaje por refuerzo'),
        ('deep_learning', 'Deep Learning'),
        ('time_series', 'Series temporales'),
    ]
    ai_type = models.CharField(
        "Tipo de Inteligencia Artificial",
        max_length=30,
        choices=AI_TYPE_CHOICES,
        blank=True,
        null=True
    )

    requires_gpu = models.BooleanField(
        "¿Requiere GPU?",
        default=False,
        help_text="Indica si el proyecto necesita procesamiento con GPU"
    )

    # Datos técnicos del modelo
    model_accuracy = models.DecimalField(
        "Precisión del modelo (%)",
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Precisión o métrica relevante del modelo"
    )
    decision_maps = models.TextField(
        "Mapas de decisión / diagramas",
        blank=True,
        null=True,
        help_text="Descripción o links a mapas de decisión, diagramas de árbol, u otras visualizaciones"
    )
    technical_notes = models.TextField(
        "Notas técnicas adicionales",
        blank=True,
        null=True,
        help_text="Información técnica para garantizar la escalabilidad y confiabilidad del modelo"
    )

    # 👤 Desarrollador asignado
    assigned_developer = models.ForeignKey(
        SmartQuailCrew,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_intelligences',
        verbose_name="Desarrollador asignado"
    )

    # 📅 Fechas
    start_date = models.DateField("Fecha de inicio", null=True, blank=True)
    delivery_date = models.DateField("Fecha de entrega", null=True, blank=True)

    approved_by_client = models.BooleanField("¿Aprobado por cliente?", default=False)

    final_url = models.URLField("URL final", blank=True, null=True)

    # 🕓 Cálculo de duración
    total_development_days = models.PositiveIntegerField(
        "Días de desarrollo", null=True, blank=True, editable=False
    )

    def save(self, *args, **kwargs):
        if self.start_date and self.delivery_date:
            delta = self.delivery_date - self.start_date
            self.total_development_days = delta.days if delta.days >= 0 else 0
        else:
            self.total_development_days = None
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.project.name}"



class QATest(models.Model):
    process = models.ForeignKey(BusinessProcess, on_delete=models.CASCADE, related_name='qa_tests')
    test_case = models.CharField(max_length=255)
    description = models.TextField()
    result = models.CharField(max_length=50, choices=[('passed', 'Aprobado'), ('failed', 'Fallido'), ('pending', 'Pendiente')])
    executed_at = models.DateTimeField(auto_now_add=True)
    executed_by = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.test_case} - {self.result}"


class CloudResource(models.Model):
    project = models.ForeignKey(BusinessSystemProject, on_delete=models.CASCADE, related_name='cloud_resources')
    
    RESOURCE_TYPES = [
        ('compute', 'Compute (VM, EC2, etc.)'),
        ('storage', 'Almacenamiento'),
        ('database', 'Base de Datos'),
        ('network', 'Red'),
        ('other', 'Otro'),
    ]

    resource_type = models.CharField(max_length=50, choices=RESOURCE_TYPES)
    provider = models.CharField(max_length=100)  # Ej: AWS, GCP, Azure
    resource_name = models.CharField(max_length=100)
    monthly_cost_usd = models.DecimalField(max_digits=10, decimal_places=2)

    monitoring_tool = models.CharField(max_length=100, blank=True, null=True)
    monitoring_status = models.CharField(max_length=50, choices=[('healthy', 'Operativo'), ('warning', 'Advertencia'), ('critical', 'Crítico')], default='healthy')
    alert_summary = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.resource_name} ({self.provider})"
