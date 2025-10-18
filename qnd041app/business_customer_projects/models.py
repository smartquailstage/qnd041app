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


class BusinessProcess(models.Model):
    project = models.ForeignKey(BusinessSystemProject, on_delete=models.CASCADE, related_name='processes')
    name = models.CharField(max_length=200)
    description = models.TextField()

    progress = models.IntegerField(help_text="Progreso del 0 al 100 (%)")

    has_automation = models.BooleanField(default=False)
    automation_description = models.TextField(blank=True, null=True)

    has_ai = models.BooleanField(default=False)
    ai_model_description = models.TextField(blank=True, null=True, help_text="Describe el modelo de IA y su implementación en el proceso")

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
