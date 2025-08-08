from django.db import models

class Servicio(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    costo_adicional = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        help_text="Costo adicional fijo del servicio (en USD)"
    )

    def __str__(self):
        return self.nombre

class Estimacion(models.Model):
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    usuarios_estimados = models.PositiveIntegerField()
    tipo_uso = models.CharField(max_length=50, choices=[
        ('transaccional', 'Transaccional'),
        ('analitico', 'Analítico'),
        ('mixto', 'Mixto'),
    ])
    proveedor = models.CharField(max_length=50, choices=[
        ('aws', 'AWS'),
        ('azure', 'Azure'),
        ('gcp', 'GCP'),
    ])
    fecha = models.DateTimeField(auto_now_add=True)

    # Resultados estimados
    vcpu = models.FloatField()
    ram_gb = models.FloatField()
    almacenamiento_gb = models.FloatField()
    costo_estimado = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Estimación {self.id} - {self.servicio.nombre}"