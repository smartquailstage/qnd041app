from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from usuarios.models  import SmartQuailCrew


class BusinessSystemProject(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    # ✅ Relación con el equipo de SmartQuail
    crew_members = models.ManyToManyField(
        'usuarios.SmartQuailCrew',
        related_name='projects',
        blank=True,
        verbose_name='Equipo asignado'
    )


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
