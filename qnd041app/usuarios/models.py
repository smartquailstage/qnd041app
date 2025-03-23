from django.db import models
from django.conf import settings
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from localflavor.ec.forms import ECProvinceSelect
from ckeditor.fields import RichTextField
from django.core.cache import cache
from django.contrib.auth.models import User, Group
from django.core.validators import RegexValidator

class Perfil_Terapeuta(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Nombre de Usuario")
    especialidad = models.CharField(max_length=255, blank=True, null=True, verbose_name="Especialidad")

    class Meta:
        ordering = ['user']
        verbose_name_plural = "Perfiles de Terapeutas"

    def __str__(self):
        return 'Perfil de terapeuta {}'.format(self.user.username)



class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Nombre de Usuario")
    activity = models.CharField(blank=True, null=True, max_length=120, choices=[("PACIENTE", "Paciente"), ("TERAPEUTA", "Terapeuta")], verbose_name="Tipo de usuario")
    #user_group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True,verbose_name="¿Que actividad cultural desea realizar en nuestra plataforma?")
    representante_legal_nombre = models.CharField(max_length=255, blank=True, null=True, verbose_name="Nombre del Representante")
    representante_legal_apellido = models.CharField(max_length=255, blank=True, null=True, verbose_name="Nombre del Representante")
    nombre_factura= models.CharField(max_length=255, blank=True, null=True, verbose_name="Nombre de la factura")
    ruc = models.CharField(max_length=13, verbose_name="RUC / C.I", help_text="R.U.C o C.I del Representante",blank=True, null=True)
    email = models.EmailField(blank=True, null=True, verbose_name="Email")
    phone_regex = RegexValidator(
        regex=r'^\+?593?\d{9,15}$',
        message="El número de teléfono debe estar en formato internacional. Ejemplo: +593XXXXXXXXX."
    )
    telefono = PhoneNumberField(verbose_name="Teléfon de contacto",validators=[phone_regex],default='+593')
    direccion = models.CharField(max_length=255, blank=True, null=True, verbose_name="Drección")
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True, verbose_name="Foto de Paciente")
    date_of_birth = models.DateField(blank=True, null=True, verbose_name="Fecha de Nacimiento del paciente")
    Paciente_nombre = models.CharField(max_length=255, blank=True, null=True, verbose_name="Nombre del Representante")
    unidad_educativa =  models.CharField(max_length=255, blank=True, null=True, verbose_name="Unidad educativa del paciente")
    ruc = models.CharField(max_length=13, verbose_name="RUC / C.I", help_text="C.I del Paciente",blank=True, null=True)
    curso = models.CharField(max_length=255, blank=True, null=True, verbose_name="curso o Paralelo")
    nacionalidad = models.CharField(blank=True, null=True, max_length=100, verbose_name="Nacionalidad del Paciente")
    sexo = models.CharField(blank=True, null=True, max_length=120, choices=[("MASCULINO", "Masculino"), ("FEMENINO", "Femenino")], verbose_name="Sexo del Paciente")
    user_terapeuta = models.OneToOneField(Perfil_Terapeuta, on_delete=models.CASCADE, verbose_name="Terapeuta Asignado")

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