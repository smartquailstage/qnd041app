from django.db import models
from django.conf import settings
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from localflavor.ec.forms import ECProvinceSelect
from ckeditor.fields import RichTextField
from django.core.cache import cache
from django.contrib.auth.models import User, Group
from django.core.validators import RegexValidator
from datetime import date
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField
from django_celery_results.models import TaskResult
from djmoney.models.fields import MoneyField
from django.core.validators import FileExtensionValidator
from django.utils import timezone
from datetime import timedelta
from schedule.models import Event, Calendar
from django.utils.datetime_safe import datetime
from django.utils.timezone import make_aware
from usuarios.models import Profile

# Create your models here.
class Cita(models.Model):
    creador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='crear_citas',
        on_delete=models.CASCADE
    )
    destinatario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='recibir_citas',
        on_delete=models.CASCADE
    )
    fecha = models.DateTimeField()
    fecha_final = models.DateTimeField(null=True, blank=True)
    motivo = models.CharField(max_length=255)
    estado = models.CharField(
        max_length=20,
        choices=[
            ('pendiente', 'Pendiente'),
            ('confirmada', 'Confirmada'),
            ('cancelada', 'Cancelada'),
        ],
        default='pendiente'
    )
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    notas = models.TextField(blank=True, null=True)
    paciente = models.ForeignKey(Profile, on_delete=models.CASCADE,null=True, blank=True,  related_name='perfil_paciente',)
    sucursal = models.CharField(max_length=255,blank=True,null=True,
        choices=[
            ('Quito - Valles', 'Quito - Valles'),
            ('Quito - Centro', 'Quito - Centro'),
            ('Guayaquil', 'Guayaquil'),
            ('Manta', 'Manta'),
        ],
        verbose_name="Sucursal"
    )
    

    class Meta:
        
        ordering = ['-fecha']
        verbose_name_plural = "Registros Administrativos / Ingreso de Citas"
        verbose_name = "Administrativos / Ingreso de Cita"

def __str__(self):
    return f"{self.creador} → {self.destinatario} ({self.fecha.strftime('%d/%m/%Y %H:%M')})"
