from django.db import models
from djmoney.models.fields import MoneyField
# Create your models here.



class ServicioTerapeutico(models.Model):

    LUGAR_CHOICES = [
        ('INSTITUCIONAL', 'Institucional'),
        ('DOMICILIO', 'Domicilio'),
        ('CONSULTA', 'Consulta'),
    ]


    TIPO_SERVICIO = [
    # Terapias principales
    ('TERAPIA_DE_LENGUAJE', 'Terapia de Lenguaje'),
    ('ESTIMULACION_COGNITIVA', 'Estimulación Cognitiva'),
    ('TERAPIA_OCUPACIONAL', 'Terapia Ocupacional'),

    # Psicología (subtipos incluidos)
    ('PSICOLOGIA_PAREJA', 'Psicología - Pareja'),
    ('PSICOLOGIA_INFANTIL', 'Psicología - Infantil'),
    ('PSICOLOGIA_FAMILIAR', 'Psicología - Familiar'),
    ('PSICOLOGIA_ADULTOS', 'Psicología - Adultos'),

    # Valoraciones
    ('VALORACION_PSICOLOGICA', 'Valoración Psicológica'),
    ('VALORACION_LENGUAJE', 'Valoración de Lenguaje'),

    # Estimulación
    ('ESTIMULACION_TEMPRANA', 'Estimulación Temprana'),

    # Otros servicios clínicos
    ('AUDIOLOGIA', 'Audiología'),
    ('OPTOMETRIA_OFTALMOLOGIA', 'Optometría / Oftalmología'),
    ]


    lugar_servicio = models.CharField(
        max_length=50,
        choices=LUGAR_CHOICES,
        default='INSTITUCIONAL',
        verbose_name="Lugar donde se ofrece el servicio"
    )

    servicio = models.CharField(
        max_length=255,
        choices=TIPO_SERVICIO,
        verbose_name="Servicio terapéutico"
    )

    costo_por_sesion = MoneyField(
        max_digits=10,
        decimal_places=2,
        default_currency='USD',  # o 'PEN', 'ARS', etc.
        blank=True,
        null=True,
        verbose_name="Valor por sesión"
    ) 

    observacion = models.TextField(blank=True, null=True, verbose_name="Escriba Detalle del servicio")

    activo = models.BooleanField(default=True, verbose_name="¿Servicio activo?")

    class Meta:
        verbose_name = "Servicio Terapéutico"
        verbose_name_plural = "Servicios Terapéuticos"
        ordering = ['servicio']

    def __str__(self):
        return f"{self.servicio} - {self.lugar_servicio}"