from django.db import models
import hashlib
import uuid


class Contrato(models.Model):

    TIPO_CONTRATO_CHOICES = [
        ('CONF', 'Acuerdo de confidencialidad y no competencia'),
        ('LAB', 'Contrato laboral'),
        ('ASA', 'Acta de asamblea'),
        ('ALI', 'Alianza estratégica'),
        ('DES', 'DECISIÓN DEL ACCIONISTA ÚNICO'),
        ('ACE', 'ACEPTACIÓN DE LOS CARGOS DE PRESIDENTE Y GERENTE GENERAL'),
        ('NON', 'NOMBRAMIENTO DE GERENTE GENERAL Y PRESIDENTE'),
        ('DE-MIT', 'DECLARACIÓN FORMAL ANTE EL MINISTERIO DE TRABAJO'),
    ]


    numero_contrato = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Número de contrato"
    )

    contract_hash = models.CharField(
        max_length=64,
        unique=True,
        null=True,
        blank=True,
        editable=True,
        db_index=True,
        verbose_name="Hash único del contrato"
    )

    tipo_contrato = models.CharField(
        max_length=200,
        choices=TIPO_CONTRATO_CHOICES,
        verbose_name="Tipo de contrato",
    )

    fecha_firma = models.DateField(verbose_name="Fecha de firma")
    fecha_inicio = models.DateField(verbose_name="Fecha de inicio")
    fecha_fin = models.DateField(blank=True, null=True, verbose_name="Fecha de finalización")

    partes_contratantes = models.TextField(verbose_name="Partes contratantes")
    objeto_contrato = models.TextField(verbose_name="Objeto del contrato")

    estado = models.CharField(
        max_length=20,
        choices=[
            ('VIGENTE', 'Vigente'),
            ('VENCIDO', 'Vencido'),
            ('RESCINDIDO', 'Rescindido'),
        ],
        default='VIGENTE',
        verbose_name="Estado del contrato"
    )

    observaciones = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.contract_hash:
            unique_string = f"{self.numero_contrato}-{uuid.uuid4()}"
            self.contract_hash = hashlib.sha256(unique_string.encode('utf-8')).hexdigest()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.numero_contrato} - {self.get_tipo_contrato_display()}"



class ClausulaContrato(models.Model):

    CLAUSULA_CHOICES = [
        ('CLAUSULA_1', 'CLÁUSULA PRIMERA'),
        ('CLAUSULA_2', 'CLÁUSULA SEGUNDA'),
        ('CLAUSULA_3', 'CLÁUSULA TERCERA'),
        ('CLAUSULA_4', 'CLÁUSULA CUARTA'),
        ('CLAUSULA_5', 'CLÁUSULA QUINTA'),
        ('CLAUSULA_6', 'CLÁUSULA SEXTA'),
        ('CLAUSULA_7', 'CLÁUSULA SÉPTIMA'),
        ('CLAUSULA_8', 'CLÁUSULA OCTAVA'),
        ('CLAUSULA_9', 'CLÁUSULA NOVENA'),
        ('CLAUSULA_10', 'CLÁUSULA DÉCIMA'),
        ('CLAUSULA_11', 'CLÁUSULA UNDÉCIMA'),
        ('CLAUSULA_12', 'CLÁUSULA DUODÉCIMA'),
        ('CLAUSULA_13', 'CLÁUSULA DECIMOTERCERA'),
        ('CLAUSULA_14', 'CLÁUSULA DECIMOCUARTA'),
        ('CLAUSULA_15', 'CLÁUSULA DECIMOQUINTA'),
        ('CLAUSULA_16', 'CLÁUSULA DECIMOSEXTA'),
        ('CLAUSULA_17', 'CLÁUSULA DECIMOSÉPTIMA'),
        ('CLAUSULA_18', 'CLÁUSULA DECIMOCTAVA'),
        ('CLAUSULA_19', 'CLÁUSULA DECIMONOVENA'),
        ('CLAUSULA_20', 'CLÁUSULA VIGÉSIMA'),
        ('CLAUSULA_21', 'CLÁUSULA VIGESIMOPRIMERA'),
        ('CLAUSULA_22', 'CLÁUSULA VIGESIMOSEGUNDA'),
        ('CLAUSULA_23', 'CLÁUSULA VIGESIMOTERCERA'),
        ('CLAUSULA_24', 'CLÁUSULA VIGESIMOCUARTA'),
        ('CLAUSULA_25', 'CLÁUSULA VIGESIMOQUINTA'),
        ('CLAUSULA_26', 'CLÁUSULA VIGESIMOSEXTA'),
        ('CLAUSULA_27', 'CLÁUSULA VIGESIMOSÉPTIMA'),
        ('CLAUSULA_28', 'CLÁUSULA VIGESIMOCTAVA'),
        ('CLAUSULA_29', 'CLÁUSULA VIGESIMONOVENA'),
        ('CLAUSULA_30', 'CLÁUSULA TRIGÉSIMA'),
    ]

    titulo_clausura = models.CharField(
        max_length=260,
        verbose_name="titulo de clausura",
        null = 'True',
        blank = 'True',
    )

    contrato = models.ForeignKey(
        Contrato,
        on_delete=models.CASCADE,
        related_name='clausulas',
        verbose_name="Contrato"
    )

    clausula = models.CharField(
        max_length=16,
        choices=CLAUSULA_CHOICES,
        verbose_name="CLÁUSULA",
        null = 'True',
        blank = 'True',
    )


    detalle = models.TextField(
        verbose_name="Detalle de la cláusula"
    )

    class Meta:
        verbose_name = "Cláusula de contrato"
        verbose_name_plural = "Cláusulas de contrato"



    def __str__(self):
        return f"Cláusula {self.clausula} - {self.contrato.numero_contrato}"
