from django.db import models
#from pgvector.django import VectorField


class Edificio(models.Model):
    nombre = models.CharField(max_length=150, unique=True)
    codigo = models.SlugField(unique=True)
    direccion = models.CharField(max_length=255)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class AreaComun(models.Model):
    class TipoArea(models.TextChoices):
        LOBBY = "lobby", "Lobby y recepción"
        ASCENSORES = "ascensores", "Ascensores"
        GARAJE = "garaje", "Garaje y accesos"
        TERRAZA = "terraza", "Terraza y áreas sociales"
        JARDINES = "jardines", "Jardines y exteriores"
        OTRO = "otro", "Otra área común"

    edificio = models.ForeignKey(Edificio, on_delete=models.CASCADE, related_name="areas_comunes")
    nombre = models.CharField(max_length=120)
    tipo_area = models.CharField(max_length=30, choices=TipoArea.choices)
    frecuencia_limpieza_dias = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.edificio.codigo} - {self.nombre}"


class RegistroLimpieza(models.Model):
    class Estado(models.TextChoices):
        PROGRAMADA = "programada", "Programada"
        COMPLETADA = "completada", "Completada"
        OBSERVADA = "observada", "Observada"

    area_comun = models.ForeignKey(AreaComun, on_delete=models.CASCADE, related_name="limpiezas")
    fecha_ejecucion = models.DateField()
    responsable = models.CharField(max_length=120)
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.COMPLETADA)
    observaciones = models.TextField(blank=True)

    class Meta:
        ordering = ["-fecha_ejecucion", "-id"]


class OrdenMantenimiento(models.Model):
    class TipoMantenimiento(models.TextChoices):
        PREVENTIVO = "preventivo", "Preventivo"
        CORRECTIVO = "correctivo", "Correctivo"

    class Estado(models.TextChoices):
        PENDIENTE = "pendiente", "Pendiente"
        EN_PROCESO = "en_proceso", "En proceso"
        CERRADO = "cerrado", "Cerrado"

    edificio = models.ForeignKey(Edificio, on_delete=models.CASCADE, related_name="mantenimientos")
    area_comun = models.ForeignKey(
        AreaComun, on_delete=models.SET_NULL, null=True, blank=True, related_name="mantenimientos"
    )
    tipo = models.CharField(max_length=20, choices=TipoMantenimiento.choices)
    titulo = models.CharField(max_length=180)
    descripcion = models.TextField(blank=True)
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.PENDIENTE)
    fecha_programada = models.DateField()
    fecha_cierre = models.DateField(null=True, blank=True)
    costo_estimado = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    costo_real = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    class Meta:
        ordering = ["-fecha_programada", "-id"]


class Unidad(models.Model):
    edificio = models.ForeignKey(Edificio, on_delete=models.CASCADE, related_name="unidades")
    codigo = models.CharField(max_length=40)
    piso_o_torre = models.CharField(max_length=60, blank=True)
    alicuota_porcentaje = models.DecimalField(max_digits=6, decimal_places=4)

    class Meta:
        unique_together = ("edificio", "codigo")

    def __str__(self):
        return f"{self.edificio.codigo} - {self.codigo}"


class CargoAlicuota(models.Model):
    class EstadoPago(models.TextChoices):
        PENDIENTE = "pendiente", "Pendiente"
        PARCIAL = "parcial", "Pago parcial"
        PAGADO = "pagado", "Pagado"
        VENCIDO = "vencido", "Vencido"

    unidad = models.ForeignKey(Unidad, on_delete=models.CASCADE, related_name="cargos_alicuota")
    periodo = models.CharField(max_length=7, help_text="Formato YYYY-MM")
    monto_alicuota = models.DecimalField(max_digits=12, decimal_places=2)
    monto_expensas_extra = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    monto_pagado = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    estado = models.CharField(max_length=20, choices=EstadoPago.choices, default=EstadoPago.PENDIENTE)
    fecha_vencimiento = models.DateField()

    class Meta:
        unique_together = ("unidad", "periodo")
        ordering = ["-periodo", "unidad__codigo"]


class DocumentoNormativo(models.Model):
    class TipoDoc(models.TextChoices):
        LEY_PH = "ley_propiedad_horizontal", "Ley de Propiedad Horizontal"
        REGLAMENTO = "reglamento_interno", "Reglamento Interno"

    edificio = models.ForeignKey(
        Edificio, on_delete=models.CASCADE, null=True, blank=True, related_name="documentos_normativos"
    )
    tipo_documento = models.CharField(max_length=40, choices=TipoDoc.choices)
    titulo = models.CharField(max_length=200)
    vigente = models.BooleanField(default=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titulo


class FragmentoNormativo(models.Model):
    documento = models.ForeignKey(
        DocumentoNormativo, on_delete=models.CASCADE, related_name="fragmentos"
    )
    referencia = models.CharField(max_length=120, help_text="Ej. Art. 14 / Capítulo III")
    contenido = models.TextField()
    #embedding = VectorField(dimensions=768, null=True, blank=True)

    class Meta:
        indexes = [models.Index(fields=["referencia"])]