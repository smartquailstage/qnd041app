from django.db import models
from django.conf import settings
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from localflavor.ec.forms import ECProvinceSelect
from ckeditor.fields import RichTextField
from django.core.cache import cache
from django.contrib.auth.models import User, Group
from django.core.validators import RegexValidator
from django.core.validators import MinValueValidator, MaxValueValidator


class Edificio(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Nombre de Usuario")
    especialidad = models.CharField(max_length=255, blank=True, null=True, verbose_name="Especialidad")
    
    # Campo para el presupuesto (valor tipo divisa)
    presupuesto = models.DecimalField(
        max_digits=10,  # Ajusta según el tamaño del presupuesto
        decimal_places=2,
        blank=False,
        null=False,
        verbose_name="Presupuesto del Edificio",
        validators=[MinValueValidator(0)]  # Aseguramos que el valor sea positivo
    )
    
    # Campo para el factor K (valor numérico)
    k = models.DecimalField(
        max_digits=5,  # Tamaño máximo del número
        decimal_places=2,
        blank=False,
        null=False,
        verbose_name="Factor K",
        validators=[MinValueValidator(0.01), MaxValueValidator(10)]  # Ajusta los límites del factor K
    )

    # Método para calcular los puntos máximos que una persona puede tener para el descuento total
    @property
    def puntos_maximos(self):
        """
        Calcula la cantidad máxima de puntos que una persona puede tener para calificar
        para el descuento total, basado en el presupuesto y el factor K.
        """
        if self.presupuesto and self.k:
            # Suponemos que los puntos máximos son directamente proporcionales al presupuesto
            # multiplicado por el factor k. Este cálculo puede ajustarse según el negocio.
            puntos_maximos = self.presupuesto * self.k
            return puntos_maximos
        return 0

    # Método para determinar si la persona califica para el descuento total
    def calificar_descuento(self, puntos_persona):
        """
        Determina si la persona califica para el descuento total en la alícuota
        dependiendo de los puntos que tenga.
        """
        if puntos_persona >= self.puntos_maximos:
            return True  # Califica para el descuento
        return False

    # Método para calcular los puntos mínimos, si es necesario (aunque no se menciona en el caso)
    @property
    def puntos_minimos(self):
        """
        Calcula la cantidad mínima de puntos necesarios para el descuento total.
        """
        if self.presupuesto and self.k:
            # El mínimo de puntos también puede depender del presupuesto y el factor k
            # Ajusta esta fórmula según lo que requiera tu lógica de negocio.
            puntos_minimos = self.presupuesto / self.k
            return puntos_minimos
        return 0

    class Meta:
        ordering = ['user']
        verbose_name_plural = "Perfil de Edificios"

    def __str__(self):
        return 'Perfil de terapeuta {}'.format(self.user.username)



class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Nombre de Usuario")
    activity = models.CharField(blank=True, null=True, max_length=120, choices=[("PACIENTE", "Paciente"), ("TERAPEUTA", "Terapeuta")], verbose_name="Tipo de usuario")
    representante_legal_nombre = models.CharField(max_length=255, blank=True, null=True, verbose_name="Nombre del Representante")
    representante_legal_apellido = models.CharField(max_length=255, blank=True, null=True, verbose_name="Apellido del Representante")
    nombre_factura = models.CharField(max_length=255, blank=True, null=True, verbose_name="Nombre de la factura")
    ruc = models.CharField(max_length=13, verbose_name="RUC / C.I", help_text="R.U.C o C.I del Representante", blank=True, null=True)
    email = models.EmailField(blank=True, null=True, verbose_name="Email")
    telefono = models.CharField(max_length=20, blank=True, null=True, verbose_name="Teléfono de contacto")
    direccion = models.CharField(max_length=255, blank=True, null=True, verbose_name="Dirección")
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True, verbose_name="Foto de Usuario")
    date_of_birth = models.DateField(blank=True, null=True, verbose_name="Fecha de Nacimiento")
    # Otros campos...
    class Meta:
        ordering = ['user']
        verbose_name_plural = "Perfiles de Usuario"

    def __str__(self):
        return 'Perfil de Usuario {}'.format(self.user.username)
    

class Dashboard(models.Model):
    titulo = models.CharField(max_length=100)
    informacion_basica = RichTextField()
    bloque_1 = RichTextField(blank=True, null=True)
    bloque_2 = RichTextField(blank=True, null=True)
    bloque_3 = RichTextField(blank=True, null=True)
    bloque_4 = RichTextField(blank=True, null=True)
    bloque_5 = RichTextField(blank=True, null=True)
    link_soporte_tecnico = models.URLField()

    def __str__(self):
        return self.titulo
    title = models.CharField(max_length=100)
    content = models.TextField()
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title