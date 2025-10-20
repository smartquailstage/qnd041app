from django.db import models

# Suponiendo que el modelo SmartService está en otro archivo
from servicios.models import SmartService


class Contratante(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='contratante_info')
    ruc = models.CharField(max_length=13, unique=True)
    direccion = models.TextField()
    telefono = models.CharField(max_length=20)
    correo = models.EmailField()

    def __str__(self):
        return self.nombre


class ITCloudContratante(models.Model):
    nombre_contacto = models.CharField(max_length=255)
    cargo = models.CharField(max_length=100)
    correo = models.EmailField()
    telefono = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.nombre_contacto} ({self.cargo})"


class Contrato(models.Model):
    numero_contrato = models.CharField(max_length=50, unique=True)
    fecha_firma = models.DateField()
    
    contratante = models.ForeignKey(Contratante, on_delete=models.CASCADE)
    servicios = models.ManyToManyField(SmartService)
    itcloud_contratante = models.ForeignKey(ITCloudContratante, on_delete=models.CASCADE)

    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Contrato #{self.numero_contrato}"


class Clausula(models.Model):
    contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE, related_name='clausulas')
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()

    orden = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['orden']

    def __str__(self):
        return f"{self.orden}. {self.titulo}"
