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
#from schedule.models import Event, Calendar
from django.utils.datetime_safe import datetime
from django.utils.timezone import make_aware
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from django.core.exceptions import ValidationError
from tinymce.models import HTMLField
from django.contrib.auth.models import AbstractUser
from serviceapp.models import ServicioTerapeutico
from decimal import Decimal
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from django.conf import settings


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Debe ingresar un correo electrónico')
        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name="Correo Electrónico")
    first_name = models.CharField(max_length=30, blank=True, verbose_name="Nombres")
    last_name = models.CharField(max_length=150, blank=True, verbose_name="Apellidos") 
    is_active = models.BooleanField(default=True, verbose_name="Es activo")
    is_staff = models.BooleanField(default=False, verbose_name="Es Staff")

    # 👇 Campos nuevos
    acepta_terminos = models.BooleanField(
        default=False,
        verbose_name="Acepta los términos y condiciones"
    )
    suscripcion_noticias = models.BooleanField(
        default=False,
        verbose_name="Desea suscribirse al canal de noticias"
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    @property
    def username(self):
        return self.email

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self):
        return self.first_name




from django.db import models
from django.conf import settings
from djmoney.models.fields import MoneyField
from phonenumber_field.modelfields import PhoneNumberField
from decimal import Decimal
from datetime import date

class SmartQuailCrew(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # Información personal
    full_name = models.CharField("Nombre completo", max_length=100)
    date_of_birth = models.DateField("Fecha de nacimiento")

    # ✅ Foto de perfil
    profile_picture = models.ImageField(
    "Foto de perfil",
    upload_to="crew/profile_pictures/",
    blank=True,
    null=True
    )

    gender_choices = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    ]
    gender = models.CharField("Género", max_length=1, choices=gender_choices)

    national_id = models.CharField("Identificación nacional", max_length=20, unique=True)

    phone = PhoneNumberField("Teléfono", default='+593')
    email = models.EmailField("Correo electrónico", unique=True)
    address = models.CharField("Dirección", max_length=255)

    # Rol en el equipo
    ROLE_CHOICES = [
        ('developer', 'Desarrollador'),
        ('engineer', 'Ingeniero'),
        ('content_creator', 'Creador de Contenido'),
        ('architect', 'Arquitecto de Software'),
        ('project_manager', 'Project Manager'),
        ('product_manager', 'Product Manager'),
        ('qa_engineer', 'QA Engineer'),
        ('ux_ui', 'Diseñador UX/UI'),
        ('data_scientist', 'Científico de Datos'),
    ]
    role = models.CharField("Rol", max_length=30, choices=ROLE_CHOICES)

    # Horas y pagos
    total_hours_worked = models.DecimalField("Horas trabajadas", max_digits=6, decimal_places=2, default=0.0)
    hourly_rate = MoneyField("Costo por hora", max_digits=10, decimal_places=2, default_currency='USD')
    total_cost = MoneyField("Costo total a pagar", max_digits=12, decimal_places=2, default_currency='USD', editable=False)

    # Contrato
    contract_type_choices = [
        ('FT', 'Tiempo completo'),
        ('PT', 'Medio tiempo'),
        ('CT', 'Contrato temporal'),
        ('FREELANCE', 'Freelancer'),
    ]
    contract_type = models.CharField("Tipo de contrato", max_length=10, choices=contract_type_choices)

    # Documentos personales y laborales
    resume = models.FileField("Hoja de vida", upload_to='crew/resumes/', blank=True, null=True)
    portfolio = models.FileField("Portafolio", upload_to='crew/portfolios/', blank=True, null=True)
    work_contract = models.FileField("Contrato laboral", upload_to='crew/contracts/', blank=True, null=True)
    nda_contract = models.FileField("Contrato de confidencialidad (NDA)", upload_to='crew/nda/', blank=True, null=True)

    # Estado
    is_active = models.BooleanField("Activo", default=True)

    PAYMENT_METHOD_CHOICES = [
        ('transfer', 'Transferencia bancaria'),
        ('platform', 'Plataforma de pagos'),
        ('cash', 'Efectivo'),
    ]
    payment_method = models.CharField("Método de pago", max_length=20, choices=PAYMENT_METHOD_CHOICES,blank=True,null=True)

    # Solo si es transferencia
    bank_transaction_number = models.CharField(
        "Número de transacción bancaria",
        max_length=50,
        blank=True,
        null=True
    )
    bank_info = models.CharField(
        "Información bancaria (Banco, cuenta, etc.)",
        max_length=255,
        blank=True,
        null=True
    )

    # Solo si es plataforma
    payment_platform_info = models.CharField(
        "Plataforma de pago (nombre, ID)",
        max_length=255,
        blank=True,
        null=True
    )

    # Timestamps
    created_at = models.DateTimeField("Creado", auto_now_add=True)
    updated_at = models.DateTimeField("Actualizado", auto_now=True)

    # Métodos de pago


    # ... [resto del modelo] ...
 

    class Meta:
        verbose_name = "Miembro del equipo SmartQuail"
        verbose_name_plural = "SmartQuail Crew"

    def __str__(self):
        return f"{self.full_name} - {self.get_role_display()}"

    def save(self, *args, **kwargs):
        if self.total_hours_worked and self.hourly_rate:
            self.total_cost = Decimal(self.total_hours_worked) * self.hourly_rate.amount
        else:
            self.total_cost = Decimal('0.00')
        super().save(*args, **kwargs)

    @property
    def age(self):
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )




class AdministrativeProfile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField("Fecha de nacimiento")
    gender_choices = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    ]
    gender = models.CharField("Género", max_length=1, choices=gender_choices)
    national_id = models.CharField("Cédula de identidad", max_length=20, unique=True)
    phone_regex = RegexValidator(
        regex=r'^\+?593?\d{9,15}$',
        message="El número de teléfono debe estar en formato internacional. Ejemplo: +593XXXXXXXXX."
    )
    telefono = PhoneNumberField(
        verbose_name="Teléfono de la Institución",
        validators=[phone_regex],
        default='+593'
    )
    email = models.EmailField("Correo electrónico", unique=True)
    address = models.CharField("Direccion de Domicilio", max_length=200, unique=True)

    # Información administrativa
    DEPARTMENT_CHOICES = [
        ('gerencia', 'Gerencia'),
        ('administracion', 'Administración'),
        ('financiero', 'Financiero'),
         ('operativo', 'Operativo'),
    ]
    department = models.CharField("Departamento", max_length=30, choices=DEPARTMENT_CHOICES)

    JOB_TITLE_CHOICES = [
        # Gerencia
        ('gerente_general', 'Gerente General'),
        ('gerente_comercial', 'Ejecutivo Comercial'),
        
        # Administración
        ('tecnico_administrativo', 'Técnico Administrativo'),
        ('asistente_administrativo', 'Asistente Administrativo'),
        ('terapeuta', 'Terapéuta'),

        # Financiero
        ('contador', 'Contador'),
        ('analista_financiero', 'Analista Financiero'),
        ('jefe_finanzas', 'Jefe de Finanzas'),
    ]
    job_title = models.CharField("Cargo", max_length=50, choices=JOB_TITLE_CHOICES)

    date_joined = models.DateField("Fecha de ingreso")
    contract_type_choices = [
        ('FT', 'Tiempo completo'),
        ('PT', 'Medio tiempo'),
        ('CT', 'Contrato temporal'),
    ]
    contract_type = models.CharField("Tipo de contrato", max_length=2, choices=contract_type_choices)
    salary = MoneyField(
        max_digits=10,
        decimal_places=2,
        default_currency='USD',  # o 'PEN', 'ARS', etc.
        blank=True,
        null=True,
        verbose_name="Valor base",
        )
    is_active = models.BooleanField("Activo", default=True)

    num_pacientes_captados = models.PositiveIntegerField(
        "Pacientes captados", default=0, help_text="Número de pacientes adquiridos por este administrativo", null=True, blank=True
    )


    valor_por_paciente = MoneyField(
        "Valor por paciente", max_digits=10, decimal_places=2, default_currency='USD',
        help_text="Valor por paciente/Comisión",null=True, blank=True
    )

    # Documentación
    resume = models.FileField("Hoja de vida", upload_to='resumes/', blank=True, null=True)
   # photo = models.ImageField("Foto", upload_to='photos/', blank=True, null=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Perfil administrativo"
        verbose_name_plural = "Perfiles administrativos"



    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.get_job_title_display()}"


    
    
    @property
    def comision_total_calculada(self):
        if self.num_pacientes_captados is None or self.valor_por_paciente is None:
            return Decimal('0.00')
        return self.num_pacientes_captados * self.valor_por_paciente.amount
    
    
    @property
    def age(self):
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )

    @property
    def patients_count(self):
        return self.pacientes.count()



class Sucursal(models.Model):
    nombre = models.CharField("Nombre de la Sucursal", max_length=100)
    direccion = models.CharField("Dirección", max_length=255)
    telefonos = models.CharField("Teléfonos de Contacto", max_length=100, help_text="Separar múltiples teléfonos con comas.")
    persona_encargada = models.CharField("Persona Encargada", max_length=100)
    correo = models.EmailField("Mail de la Sucursal")

    def __str__(self):
        return self.nombre



class Prospeccion(models.Model):
    provincia = models.CharField("Provincia", max_length=100)
    nombre_institucion = models.CharField("Nombre de la Institución", max_length=255)
    estado = models.CharField("Estado", max_length=100)
    telefono = models.CharField("Teléfono", max_length=50, blank=True, null=True)
    direccion = models.CharField("Dirección", max_length=500, blank=True, null=True)
    nombre_contacto = models.CharField("Nombre de Contacto", max_length=255, blank=True, null=True)
    cargo_contacto = models.CharField("Cargo del Contacto", max_length=255, blank=True, null=True)
    email_contacto = models.CharField("Email de Contacto", max_length=255, blank=True, null=True)
    proceso_realizado = models.CharField("Proceso Realizado", max_length=500, blank=True, null=True)
    responsable = models.CharField("Responsable del contacto", max_length=255, blank=True, null=True)
    fecha_contacto = models.CharField("Fecha de Contacto", max_length=20, blank=True, null=True)
    observaciones = models.CharField("Observaciones", max_length=500, blank=True, null=True)
    fecha_proximo_contacto = models.CharField("Fecha Próximo Contacto", max_length=20, blank=True, null=True)

    class Meta:
        ordering = ['-fecha_contacto']
        verbose_name_plural = "Registros Administrativos / Prospección "
        verbose_name = "Administrativo / Prospecciones"

    def __str__(self):
        return self.nombre_institucion


class PerfilInstitucional(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    colegio = models.ForeignKey(Prospeccion, on_delete=models.SET_NULL, null=True)
    cargo = models.CharField(max_length=100, null=True, blank=True, verbose_name="Cargo del Usuario en la Institución")
    phone_regex = RegexValidator(
        regex=r'^\+?593?\d{9,15}$',
        message="El número de teléfono debe estar en formato internacional. Ejemplo: +593XXXXXXXXX."
    )
    telefono = PhoneNumberField(verbose_name="Teléfono convencional de contacto",validators=[phone_regex],default='+593')  # Puedes cambiar la región a la tuya
    correo_electronico = models.EmailField()

    def __str__(self):
        return f"{self.usuario.get_full_name()} - {self.colegio.nombre_institucion if self.colegio else 'Sin colegio'} - {self.cargo if self.cargo else 'Sin cargo'}"

    def nombre_completo(self):
        full_name = self.usuario.get_full_name()
        return full_name if full_name else self.usuario.username



class prospecion_administrativa(models.Model):
    ESTADOS = [
        ('por_contactar', 'Por Contactar'),
        ('contactado', 'Contactado'),
        ('en_cita', 'En Cita'),
        ('convenio_firmado', 'Convenio Firmado'),
        ('capacitacion', 'Capacitación'),
        ('valoracion', 'Valoración'),
        ('en_terapia', 'En Terapia'),
        ('rechazado', 'Rechazado'),
        ('finalizado', 'Finalizado'),
        ('inactivo', 'Inactivo'),
    ]

    nombre = models.ForeignKey(
        'Prospeccion',
        on_delete=models.CASCADE,
        related_name="instituciones",
        null=True,
        blank=True
    )

    es_por_contactar = models.BooleanField(default=False, verbose_name="¿Se intentó contactar?")
    es_contactado = models.BooleanField(default=False, verbose_name="¿Ya fue contactado?")
    es_en_cita = models.BooleanField(default=False, verbose_name="¿Ya tuvo cita?")
    es_convenio_firmado = models.BooleanField(default=False, verbose_name="¿Firmó convenio?")
    es_capacitacion = models.BooleanField(default=False, verbose_name="¿Recibió capacitación?")
    es_valoracion = models.BooleanField(default=False, verbose_name="¿Tuvo valoración?")
    es_en_terapia = models.BooleanField(default=False, verbose_name="¿Recibe terapia?")
    es_rechazado = models.BooleanField(default=False, verbose_name="¿Fue rechazado?")
    es_finalizado = models.BooleanField(default=False, verbose_name="¿Finalizó el proceso?")
    es_inactivo = models.BooleanField(default=False, verbose_name="Activo/Inactivo")
    fecha_activo = models.DateField(verbose_name="Fecha de Activación",null=True, blank=True)
    fecha_estado_actualizado = models.DateField(auto_now=True)

    sucursal = models.ForeignKey(
        'Sucursal',
        on_delete=models.CASCADE,
        related_name="sucursal9",
        null=True,
        blank=True
    )

    CIUDADES_ECUADOR = [(city, city) for city in [
        'Ambato', 'Arenillas', 'Atacames', 'Atuntaqui', 'Azogues', 'Babahoyo',
        'Bahía de Caráquez', 'Balzar', 'Baños de Agua Santa', 'Buena Fé', 'Calceta', 'Cañar',
        'Cariamanga', 'Catamayo', 'Cayambe', 'Chone', 'Cuenca', 'Daule', 'Durán', 'El Carmen',
        'El Guabo', 'El Triunfo', 'Esmeraldas', 'Gualaceo', 'Guaranda', 'Guayaquil',
        'Huaquillas', 'Ibarra', 'Jaramijó', 'Jipijapa', 'La Concordia', 'La Libertad',
        'La Maná', 'Latacunga', 'La Troncal', 'Loja', 'Lomas de Sargentillo', 'Macará',
        'Macas', 'Machachi', 'Machala', 'Manta', 'Milagro', 'Montalvo', 'Montecristi',
        'Naranjal', 'Naranjito', 'Nueva Loja', 'Otavalo', 'Pasaje', 'Pedernales', 'Pedro Carbo',
        'Piñas', 'Playas', 'Portoviejo', 'Puerto Baquerizo Moreno', 'Puerto Francisco de Orellana',
        'Puyo', 'Quevedo', 'Quito', 'Riobamba', 'Rosa Zárate', 'Salcedo', 'Salinas',
        'Samborondón', 'San Gabriel', 'Sangolquí', 'San Lorenzo', 'Santa Elena', 'Santa Rosa',
        'Santo Domingo de los Colorados', 'Shushufindi', 'Tena', 'Tulcán', 'Valencia',
        'Velasco Ibarra', 'Ventanas', 'Vinces', 'Yaguachi', 'Zamora'
    ]]

    ciudad = models.CharField(default='Quito' ,max_length=100, choices=CIUDADES_ECUADOR, null=True, blank=True)
    direccion = models.CharField(max_length=200, null=True, blank=True)

    mail_institucion_general = models.EmailField(blank=True, null=True, verbose_name="Mail General de la Institución")

    phone_regex = RegexValidator(
        regex=r'^\+?593?\d{9,15}$',
        message="El número de teléfono debe estar en formato internacional. Ejemplo: +593XXXXXXXXX."
    )

    telefonos_colegio = PhoneNumberField(
        verbose_name="Teléfono de la Institución",
        validators=[phone_regex],
        default='+593'
    )

    # Responsable Institucional 1
    responsable_institucional_1 = models.ForeignKey(
        PerfilInstitucional,
        on_delete=models.CASCADE,
        related_name='instituciones_asignadas',
        verbose_name="Responsable Institucional 1",
        null=True,
        blank=True
    )


    # Responsable Institucional 2
    responsable_institucional_2 = models.ForeignKey(
        PerfilInstitucional,
        on_delete=models.CASCADE,
        related_name='instituciones_asignadas2',
        verbose_name="Responsable Institucional 2",
        null=True,
        blank=True
    )


    # Terapeutas
    terapeutas_asignados = models.ManyToManyField(
        'Perfil_Terapeuta',
        related_name='instituciones_asignadas_terapeuta',
        verbose_name="Terapeutas Asignados"
    )

    # Ejecutivo Meddes
    ejecutivo_meddes = models.ForeignKey(AdministrativeProfile, on_delete=models.CASCADE,null=True, blank=True, verbose_name="Ejecutivo Meddes")
    cargo_ejecutivo_meddes = models.CharField(max_length=150, null=True, blank=True)
    telefono_ejecutivo_meddes = models.CharField(max_length=50, null=True, blank=True)
    mail_ejecutivo_meddes = models.EmailField(blank=True, null=True)
    obserciones = models.TextField(
        null=True,
        blank=True,
        verbose_name="Observaciones",
        help_text="Observaciones adicionales sobre la institución"
    )

    convenio_pdf = models.FileField(
        upload_to='convenios/',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(['pdf'])],
        help_text="Cargar archivo en PDF"
    )

    class Meta:
        ordering = ['nombre']
        verbose_name_plural = "Registros Administrativos / Ingreso perfil de institución"
        verbose_name = "Administrativo / Institución"

    def alerta_estado_inactivo(self):
        if self.estado != 'inactivo':
            return False
        return timezone.now().date() - self.fecha_estado_actualizado > timedelta(days=15)

    alerta_estado_inactivo.boolean = True
    alerta_estado_inactivo.short_description = "Alerta de inactividad (15 días)"

    def __str__(self):
        return str(self.nombre) if self.nombre else "Institución sin nombre"


class DocenteCapacitado(models.Model):
    AREA_CAPACITACION = [
        ('lenguaje', 'Lenguaje'),
        ('psicologia', 'Psicología'),
    ]

    institucion = models.ForeignKey(
        prospecion_administrativa,  # Asegúrate de que esta clase esté importada correctamente
        on_delete=models.CASCADE,
        related_name="docentes_capacitados"
    )
    fecha_capacitacion = models.DateField()
    area_capacitacion = models.CharField(max_length=50, choices=AREA_CAPACITACION)
    tema = models.CharField(max_length=255)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    correo = models.EmailField()
    cedula = models.CharField(max_length=20)
    telefono = models.CharField(max_length=20)

    class Meta:
        verbose_name = "Docente Capacitado"
        verbose_name_plural = "Docentes Capacitados"

    def __str__(self):
        return f"{self.nombres} {self.apellidos} - {self.institucion.nombre}"











class Perfil_Terapeuta(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Elegir nombre de usuario en el sistema")
    especialidad = models.CharField(max_length=255, blank=True, null=True, verbose_name="Especialidad")

    SEXO_OPCIONES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    ]

    nombres_completos = models.CharField(max_length=200, null=True, blank=True)
    
    sucursal = models.ForeignKey(
        Sucursal,
        on_delete=models.CASCADE,
        related_name="sucursal10",null=True, blank=True
    )
    correo = models.EmailField(verbose_name="Correo Electrónico", null=True, blank=True)

    #edad = models.PositiveIntegerField(null=True, blank=True)
    sexo = models.CharField(max_length=1, choices=SEXO_OPCIONES, null=True, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    cedula = models.CharField(max_length=20, null=True, blank=True)
    fecha_ingreso = models.DateField(null=True, blank=True)

    titulo_universitario = models.FileField(upload_to='documentos/terapeutas/titulo/', blank=True, null=True)
    antecedentes_penales = models.FileField(upload_to='documentos/terapeutas/antecedentes/', blank=True, null=True)
    certificados = models.FileField(upload_to='documentos/terapeutas/certificados/', blank=True, null=True)

    phone_regex = RegexValidator(
        regex=r'^\+?593?\d{9,15}$',
        message="El número de teléfono debe estar en formato internacional. Ejemplo: +593XXXXXXXXX."
    )
    telefono = PhoneNumberField(verbose_name="Teléfono de persona a cargo",validators=[phone_regex],default='+593')
    TIPO_CUENTA_CHOICES = [
        ('ahorros', 'Ahorros'),
        ('corriente', 'Corriente'),
    ]

    BANCOS_ECUADOR_CHOICES = [
        ('pichincha', 'Banco Pichincha'),
        ('guayaquil', 'Banco Guayaquil'),
        ('pacifico', 'Banco del Pacífico'),
        ('produbanco', 'Produbanco'),
        ('internacional', 'Banco Internacional'),
        ('austro', 'Banco del Austro'),
        ('machala', 'Banco de Machala'),
        ('bolivariano', 'Banco Bolivariano'),
        ('promerica', 'Banco Promerica'),
        ('coopjep', 'Cooperativa JEP'),
        ('cooperco', 'Cooperco'),
        ('mutualista_pichincha', 'Mutualista Pichincha'),
        ('', 'Otro'),  # Opción para otros bancos
        # Agrega más si es necesario
    ]

    banco = models.CharField(
        "Banco", max_length=50, choices=BANCOS_ECUADOR_CHOICES,
        blank=True, null=True, help_text="Selecciona el banco"
    )
    tipo_cuenta = models.CharField(
        "Tipo de cuenta", max_length=20, choices=TIPO_CUENTA_CHOICES,
        blank=True, null=True
    )
    numero_cuenta = models.CharField("Número de cuenta", max_length=30, blank=True, null=True)
   # cedula_titular = models.CharField("Cédula del Terapeuta", max_length=20, blank=True, null=True)
    #nombre_titular = models.CharField("Nombre del titular", max_length=100, blank=True, null=True)

    servicio_domicilio = models.BooleanField(default=False, null=True, blank=True,verbose_name="Domicilio")

    pago_por_hora = MoneyField(
        max_digits=10,
        decimal_places=2,
        default_currency='USD',  # o 'PEN', 'ARS', etc.
        blank=True,
        null=True,
        verbose_name="Costo por hora Domicilio",
        )
    servicio_institucion = models.BooleanField(default=True, null=True, blank=True,verbose_name="Institución")

    pago_por_hora_institucion = MoneyField(
        max_digits=10,
        decimal_places=2,
        default_currency='USD',  # o 'PEN', 'ARS', etc.
        blank=True,
        null=True,
        verbose_name="Costo por hora Institución",
        )

    servicio_consulta = models.BooleanField(default=True, null=True, blank=True)

    pago_por_hora_consulta = MoneyField(
        max_digits=10,
        decimal_places=2,
        default_currency='USD',  # o 'PEN', 'ARS', etc.
        blank=True,
        null=True,
        verbose_name="Costo por hora Consulta",
        )

    institucional_a_domicilio = models.BooleanField(default=True, null=True, blank=True)

    pago_por_hora_institucional_a_domicilio = MoneyField(
        max_digits=10,
        decimal_places=2,
        default_currency='USD',  # o 'PEN', 'ARS', etc.
        blank=True,
        null=True,
        verbose_name="Institucional a Domicilio",
        )





    TIPO_SERVICIO = [
        ('TERAPIA DE LENGUAJE', 'Terapia de Lenguaje'),
        ('ESTIMULACIÓN COGNITIVA', 'Estimulación Cognitiva'),
        ('PSICOLOGÍA', 'Psicología'),
        ('ESTIMULACIÓN TEMPRANA', 'Estimulación Temprana'),
        ('VALORACIÓN', 'Valoración'),
        ('TERAPIA_OCUPACIONAL', 'Terapia Ocupacional'),
    ]
        
    tipos = models.JSONField(
        default=list,
        verbose_name="Tipo de servicio (múltiples opciones)",
        help_text="Selecciona uno o más tipos"
    )

    
    
    

    activo = models.BooleanField(default=True, verbose_name="¿Terapeuta activo?")
    class Meta:
        ordering = ['user']
        verbose_name = "Registro Administrativo / Ingreso de Terapista"
        verbose_name_plural = "Registro Administrativo / Ingreso de Terapista"

    @property
    def edad(self):
        today = date.today()
        if self.fecha_nacimiento:
            return today.year - self.fecha_nacimiento.year - (
                (today.month, today.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day)
            )
        return None

    def __str__(self):
        return f'{self.user.get_full_name()} - {self.especialidad}'



class ValoracionTerapia(models.Model):


    institucion = models.ForeignKey(
        'prospecion_administrativa',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Institución"
    )

    Insitucional_a_cargo = models.ForeignKey(
        PerfilInstitucional,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='valoraciones_institucionales',
        verbose_name="Institución a cargo"
    )

    es_particular = models.BooleanField(default=False, verbose_name="Valoración Particular")
    es_convenio = models.BooleanField(default=False, verbose_name="Valoración por Convenio")

    perfil_terapeuta = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='perfil_terapeuta_asignado',
        on_delete=models.CASCADE,
        verbose_name="Terapeuta Responsable",
        null=True,
        blank=True
    )

    sucursal = models.ForeignKey(
        'sucursal',
        on_delete=models.CASCADE,
        related_name="sucursal1",
        null=True,
        blank=True
    )



    fecha_valoracion = models.DateField(verbose_name="Fecha de Valoración")
    nombre = models.CharField(max_length=255, verbose_name="Nombre del Paciente Valorado")
    fecha_nacimiento = models.DateField(verbose_name="Fecha de nacimiento")

    institucion_sin = models.CharField(max_length=255, verbose_name="Nombre de institución sin convenio", blank=True, null=True)

    grado = models.CharField(max_length=100, blank=True, null=True)

    servicio = models.ForeignKey(
        'serviceapp.ServicioTerapeutico',
        on_delete=models.CASCADE,
        related_name='servicios_terapeutico_pagos',
        verbose_name="Servicio terapéutico",
        null=True,
        blank=True
    )

    proceso_terapia = models.BooleanField(default=False, verbose_name="Proceso de Terapia")
    diagnostico = HTMLField(null=True, blank=True, verbose_name="Descripción del diagnóstico")

    fecha_asesoria = models.DateField(null=True, blank=True)
    recibe_asesoria = models.BooleanField(default=False)
    necesita_terapia = models.BooleanField(default=False)
    toma_terapia = models.BooleanField(default=False)

    observaciones = HTMLField(null=True, blank=True, verbose_name="Observaciones de la valoración")

    archivo_adjunto = models.FileField(
        upload_to='valoraciones/adjuntos/',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "Valoración Terapéutica"
        verbose_name_plural = "Valoraciones Terapéuticas"
        ordering = ['-fecha_valoracion']

    def save(self, *args, **kwargs):
        if self.es_particular and self.es_convenio:
            raise ValueError("Solo una opción puede estar activa: 'particular' o 'convenio'")
        super().save(*args, **kwargs)

    def __str__(self):
        tipo = "Particular" if self.es_particular else "Convenio" if self.es_convenio else "Sin especificar"
        return f"{self.nombre}- {self.institucion} - {self.fecha_valoracion} ({tipo})"

    @property
    def edad(self):
        if not self.fecha_nacimiento:
            return None

        today = date.today()
        years = today.year - self.fecha_nacimiento.year
        months = today.month - self.fecha_nacimiento.month
        days = today.day - self.fecha_nacimiento.day

        if days < 0:
            months -= 1
        if months < 0:
            years -= 1
            months += 12

        return f"{years} año{'s' if years != 1 else ''} y {months} mes{'es' if months != 1 else ''}"


class InformesTerapeuticos(models.Model):
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='archivos_adjuntos')
    titulo = models.CharField(max_length=255, verbose_name="Título del archivo")
    archivo = models.FileField(upload_to='documentos/pacientes/', verbose_name="Archivo")
    fecha_creado = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")

    class Meta:
        verbose_name = "Informe Terapéutico"
        verbose_name_plural = "Informes Terapéuticos"

    def __str__(self):
        return self.titulo



class Profile(models.Model):
    #Informacion personal
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Nombre de Usuario")
    contrasena = models.CharField(max_length=255, blank=True, null=True, verbose_name="Actual contraseña de usuario")
    sucursales = models.ForeignKey(Sucursal,on_delete=models.CASCADE,related_name="sucursal33",null=True, blank=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True, verbose_name="Foto Perfil")
    ruc = models.CharField(max_length=13, verbose_name="C.I Paciente", help_text="Ingrese C.I del Paciente",blank=True, null=True)
    nombre_paciente = models.CharField(max_length=255, blank=True, null=True, verbose_name="Nombres")
    apellidos_paciente = models.CharField(max_length=255, blank=True, null=True, verbose_name="Apellidos")
    nacionalidad = models.CharField(blank=True, null=True, max_length=100, verbose_name="Nacionalidad")
    sexo = models.CharField(blank=True, null=True, max_length=120, choices=[("MASCULINO", "Masculino"), ("FEMENINO", "Femenino")], verbose_name="Sexo del Paciente")
    fecha_nacimiento = models.DateField(null=True, blank=True)
   # edad =  models.CharField(max_length=255, blank=True, null=True, verbose_name="Edad")
    institucion =  models.ForeignKey(
        Prospeccion,
        on_delete=models.CASCADE,
        related_name="instituciones2",null=True, blank=True
    )
    #Informacion de representante y contacto
    nombres_representante_legal = models.CharField(max_length=255, blank=True, null=True, verbose_name="Nombres")
    apellidos_representante_legal = models.CharField(max_length=255, blank=True, null=True, verbose_name="Apellidos")
    relacion_del_representante = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        choices=[
            ('Padre', 'Padre'),
            ('Madre', 'Madre'),
            ('Hermano/a', 'Hermano/a'),
            ('Tío/a', 'Tío/a'),
            ('Abuelo/a', 'Abuelo/a'),
            ('Ñeto/a', 'Ñeto/a'),
            ('Tutor/a', 'Tutor/a'),
            ('Otro', 'Otro'),
        ],
        verbose_name="Relación del representante con el paciente"
    )

    adjunto_autorizacion = models.FileField(upload_to='documentos/pacientes/autorizacion/', blank=True, null=True)
    nacionalidad_representante = models.CharField(blank=True, null=True, max_length=100, verbose_name="Nacionalidad")
    ruc_representante = models.CharField(max_length=13, verbose_name="RUC / C.I", help_text="R.U.C o C.I del Representante",blank=True, null=True)
    email = models.EmailField(blank=True, null=True, verbose_name="Correo Electrónico")
    phone_regex = RegexValidator(
        regex=r'^\+?593?\d{9,15}$',
        message="El número de teléfono debe estar en formato internacional. Ejemplo: +593XXXXXXXXX."
    )
    telefono = PhoneNumberField(verbose_name="Teléfono convencional de contacto",validators=[phone_regex],default='+593')
    celular = PhoneNumberField(verbose_name="Teléfono celular de contacto",validators=[phone_regex],default='+593')
    provincia = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        choices=[
            ('Azuay', 'Azuay'),
            ('Bolívar', 'Bolívar'),
            ('Cañar', 'Cañar'),
            ('Carchi', 'Carchi'),
            ('Chimborazo', 'Chimborazo'),
            ('Cotopaxi', 'Cotopaxi'),
            ('El Oro', 'El Oro'),
            ('Esmeraldas', 'Esmeraldas'),
            ('Galápagos', 'Galápagos'),
            ('Guayas', 'Guayas'),
            ('Imbabura', 'Imbabura'),
            ('Loja', 'Loja'),
            ('Los Ríos', 'Los Ríos'),
            ('Manabí', 'Manabí'),
            ('Morona Santiago', 'Morona Santiago'),
            ('Napo', 'Napo'),
            ('Orellana', 'Orellana'),
            ('Pastaza', 'Pastaza'),
            ('Pichincha', 'Pichincha'),
            ('Santa Elena', 'Santa Elena'),
            ('Santo Domingo de los Tsáchilas', 'Santo Domingo de los Tsáchilas'),
            ('Sucumbíos', 'Sucumbíos'),
            ('Tungurahua', 'Tungurahua'),
            ('Zamora Chinchipe', 'Zamora Chinchipe'),
        ],
        verbose_name="Localidad",
        default='Pichincha'
    )
    direccion = models.CharField(max_length=255, blank=True, null=True, verbose_name="Dirección")
    actividad_economica =  models.CharField(max_length=255, blank=True, null=True, verbose_name="Actividad económica del representante")
    
    #Informacion de Terapeutica
    
    MOTIVOS_RETIRO = [
        ('economico', 'Económico'),
        ('insatisfecho', 'Insatisfecho'),
        ('otro', 'Otro'),
    ]

    es_en_terapia = models.BooleanField(default=False, verbose_name="En terapia")
    es_retirado = models.BooleanField(default=False, verbose_name="Retirado")
    es_pausa = models.BooleanField(default=False, verbose_name="En Pausa")
    es_alta = models.BooleanField(default=False, verbose_name="En Alta")
    

    valorizacion_terapeutica = models.ForeignKey(
        ValoracionTerapia,
        on_delete=models.CASCADE,
        related_name="valoraciones_terapeuticas",
        verbose_name="Valoración Terapéutica", blank=True, null=True,
    )

    instirucional = models.ForeignKey(
        'PerfilInstitucional',
        on_delete=models.CASCADE,
        related_name="instituciones3",
        null=True,
        blank=True,
        verbose_name="Responsable Institucional"
    )

    user_terapeutas = models.ManyToManyField(
        'Perfil_Terapeuta',  # Asegúrate de que este modelo esté bien importado
        verbose_name="Elegir Terapéutas Asignados",
        related_name='asignaciones',  # Este nombre puede ser cualquiera y se usa para acceder desde el otro lado
        blank=True  # Permite que el campo sea opcional
        )
    TIPO_SERVICIO = [
        ('TERAPIA DE LENGUAJE', 'Terapia de Lenguaje'),
        ('ESTIMULACIÓN COGNITIVA', 'Estimulación Cognitiva'),
        ('PSICOLOGÍA', 'Psicología'),
        ('ESTIMULACIÓN TEMPRANA', 'Estimulación Temprana'),
        ('VALORACIÓN', 'Valoración'),
        ('TERAPIA OCUPACIONAL', 'Terápia Ocupacional'),
    ]
        
    tipos = models.JSONField(
        default=list,
        verbose_name="servicios contratados",
        help_text="Selecciona uno o más tipos"
    )

    certificado_inicio = models.FileField(
        upload_to='certificados/inicio/',
        blank=True,
        null=True,
        verbose_name="Autorización inicio Terapéutico",
    )


    fecha_inicio = models.DateField(blank=True, null=True, verbose_name="Fecha de inicio")

    # Campos opcionales según estado
    fecha_retiro = models.DateField(null=True, blank=True)
    motivo_retiro = models.CharField(max_length=50, choices=MOTIVOS_RETIRO, null=True, blank=True)
    motivo_otro = models.CharField(max_length=255, null=True, blank=True, help_text="Especifique otro motivo (si aplica)")

    

    fecha_alta = models.DateField(null=True, blank=True,verbose_name="Fecha de Alta")
    fecha_pausa = models.DateField(null=True, blank=True)
    fecha_re_inicio = models.DateField(blank=True, null=True, verbose_name="Fecha de re inicio de tratamiento")


    #Informacion de la cuenta


    class Meta:
        ordering = ['user']
        verbose_name = "Registro Administrativo / Historial de Paciente"
        verbose_name_plural = "Registro Administrativo / Historiales de Pacientes"   

    @property
    def edad_detallada(self):
        if not self.fecha_nacimiento:
            return None

        today = date.today()
        years = today.year - self.fecha_nacimiento.year
        months = today.month - self.fecha_nacimiento.month
        days = today.day - self.fecha_nacimiento.day

        if days < 0:
            months -= 1
        if months < 0:
            years -= 1
            months += 12

        return f"{years} año{'s' if years != 1 else ''} y {months} mes{'es' if months != 1 else ''}"



    @property
    def nombre_completo(self):
        return f" {self.institucion} / {self.nombre_paciente} {self.apellidos_paciente}  ".strip()

    def __str__(self):
        return self.nombre_completo


class pagos(models.Model):
    #cliente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Nombre de Usuario")
    sucursal = models.ForeignKey(
        Sucursal,
        on_delete=models.CASCADE,
        related_name="sucursal4",null=True, blank=True
    )
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE,null=True, blank=True, verbose_name="Paciente")
    servicio = models.ForeignKey(
        'serviceapp.ServicioTerapeutico',
        on_delete=models.CASCADE,
        related_name='servicios_terapeutico',
        verbose_name="Servicio terapéutico", null=True, blank=True
    )
    fecha_vencimiento = models.DateField(null=True, blank=True)
    ruc = models.CharField(max_length=13, verbose_name="R.U.C de facturación", help_text="Ingrese RUC de facturación",blank=True, null=True)
    #fecha_emision_factura = models.DateField(blank=True, null=True, verbose_name="Fecha de emisión de factura")
    numero_factura = models.CharField(max_length=255, blank=True, null=True, verbose_name="Número de Factura")
    pago = MoneyField(
    max_digits=10,
    decimal_places=2,
    default_currency='USD',  # o 'PEN', 'ARS', etc.
    blank=True,
    null=True,
    verbose_name="Saldo a cancelar"
    )
    comprobante_pago = models.FileField(
    upload_to='comprobantes/%Y/%m/%d/',
    blank=True,
    null=True,
    verbose_name="Comprobante de pago"
    )
   # cuenta = models.CharField(max_length=255, blank=True, null=True, verbose_name="Número de cuenta")
   # colegio = models.CharField(max_length=255, blank=True, null=True, verbose_name="Nombre del colegio")
#    plan = models.CharField(
#        max_length=255,
#        blank=True,
#        null=True,
#        choices=[
#            ('Institucional', 'Institucional'),
#            ('Domicilio Institucional', 'Domicilio Institucional'),
#            ('Domicilio Familiar', 'Domicilio Familiar'),
#            ('Consultorio Institucional', 'Consultorio Institucional'),
#            ('Becas(100%)', 'Becas(100%)'),
#            ('Becas(50%)', 'Becas(50%)'),
#            ('Domicilio', 'Domicilio'),
#            ('Consultorio', 'Consultorio'),
#        ],
#        verbose_name="Plan Económico"
#    )

    #convenio = models.BooleanField(default=False, verbose_name="Convenio")
    #servicio =  models.ForeignKey(
    #    'ServicioTerapeutico',
    #    on_delete=models.CASCADE,
    #    related_name='servicios_terapeuticos4',
    #    verbose_name="Servicio terapéutico",null=True, blank=True
    #)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación", help_text="Fecha en que se creó el registro de pago",null=True, blank=True)
 #   fecha_pago = models.DateField(blank=True, null=True, verbose_name="Fecha de pago")
 #   fecha_vencimiento = models.DateField(blank=True, null=True, verbose_name="Fecha de vencimiento de pago")

#    comprobante_pago = models.FileField(upload_to='comprobantes/%Y/%m/%d/', blank=True, verbose_name="Comprobante de pago")
#    numero_de_comprobante = models.CharField(max_length=255, blank=True, null=True, verbose_name="Número de comprobante de pago")
#    banco = models.CharField(
#        max_length=255,
#        blank=True,
#        null=True,
#        choices=[
#            ('Banco Pichincha', 'Banco Pichincha'),
#            ('Banco del Pacífico', 'Banco del Pacífico'),
#            ('Produbanco', 'Produbanco'),
#            ('Banco Internacional', 'Banco Internacional'),
#            ('Banco Bolivariano', 'Banco Bolivariano'),
#            ('Banco de Guayaquil', 'Banco de Guayaquil'),
#            ('Banco del Austro', 'Banco del Austro'),
#            ('Banco Solidario', 'Banco Solidario'),
#            ('Cooperativa JEP', 'Cooperativa JEP'),
#            ('Cooperativa 29 de Octubre', 'Cooperativa 29 de Octubre'),
#            ('Cooperativa Policía Nacional', 'Cooperativa Policía Nacional'),
#            ('Banco Central del Ecuador', 'Banco Central del Ecuador'),
#            ('Banco Amazonas', 'Banco Amazonas'),
#            ('Banco ProCredit', 'Banco ProCredit'),
#            ('Banco Diners Club', 'Banco Diners Club'),
#            ('Banco General Rumiñahui', 'Banco General Rumiñahui'),
#            ('Banco Coopnacional', 'Banco Coopnacional'),
#            ('Otros', 'Otros'),
#            ('No aplica', 'No aplica'),
#        ],
#        verbose_name="Institución bancaria de Pago"
#    )
 #   metodo_pago = models.CharField(
 #       max_length=255,
 #       blank=True,
 #       null=True,
 #       choices=[
 #           ('Efectivo', 'Efectivo'),
 #           ('Transferencia Bancaria', 'Transferencia Bancaria'),
 #           ('Electónica - PayPhone', 'Electónica - PayPhone'),
 #           ('Electónica - DataFast', 'Electónica - DataFast'),
 #       ],
 #       verbose_name="Método de Pago"
 #   )


    al_dia = models.BooleanField(default=False, verbose_name="Pago al día")
    pendiente = models.BooleanField(default=False, verbose_name="Pago pendiente")
    vencido = models.BooleanField(default=False, verbose_name="Pago vencido")

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Ordenes de Pago"
        verbose_name = "Orden de Pago "

    def __str__(self):
        return f"Pagos de servicio Paciente: {self.profile.nombre_paciente} {self.profile.apellidos_paciente} - Fecha: {self.created_at.strftime('%d/%m/%Y')}"

    #def save(self, *args, **kwargs):
        # Limpiar todos los estados primero
        #self.al_dia = False
        #self.pendiente = False
        #self.vencido = False

        # Determinar cuál activar
       # if self.fecha_emision_factura and self.fecha_vencimiento:
         #   diferencia = (self.fecha_vencimiento - self.fecha_emision_factura).days
         #   if self.fecha_pago:
         #       self.al_dia = True
        #    elif diferencia < 30:
       #         self.pendiente = True
      #      else:
     #           self.vencido = True

    #    super().save(*args, **kwargs)


class MultipleChoicesField(models.CharField):
    description = "Campo para múltiples opciones almacenadas como texto separado por comas"

    def __init__(self, *args, **kwargs):
        self.choices = kwargs.get('choices', [])
        kwargs['max_length'] = kwargs.get('max_length', 255)
        super().__init__(*args, **kwargs)

    def to_python(self, value):
        if isinstance(value, list):
            return value
        if value:
            return value.split(',')
        return []

    def get_prep_value(self, value):
        if isinstance(value, list):
            return ",".join(value)
        return value

    def validate(self, value, model_instance):
        if value:
            for val in value:
                if val not in dict(self.choices).keys():
                    raise ValidationError(f"Valor '{val}' no es válido")
        super().validate(value, model_instance)



class Cita(models.Model):
    sucursal = models.ForeignKey(
        'Sucursal',
        on_delete=models.CASCADE,
        related_name="sucursal8",
        null=True, blank=True
    )

    TIPO_CITA_CHOICES = [
        ('administrativa', 'Administrativa'),
        ('terapeutica', 'Terapéutica'),
        ('particular', 'Particular'),
        ('urgente', 'Urgente'),
    ]
    tipo_cita = models.CharField(
        max_length=20,
        choices=TIPO_CITA_CHOICES,
        default='terapeutica',
        verbose_name="Categoría de Cita",
        blank=True,
        null=True,
    )

    

    creador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='citas_creadas',
        on_delete=models.CASCADE,
        null=True, blank=True
    )

    destinatario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='citas_recibidas',
        null=True, blank=True,
        on_delete=models.CASCADE,
        verbose_name="Asignar cita a Administrativo"
    )




    profile = models.ForeignKey(
        'Profile',
        on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name="Asignar cita a paciente",
        related_name='Asignar_perfil_de_paciente'
    )

    profile_terapeuta = models.ForeignKey(
        'Perfil_Terapeuta',
        on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name="Asignar cita a terapeuta",
        related_name='Asignar_perfil_de_terapeuta'
    )

    nombre_paciente = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Nombre del Paciente Particular"
    )

    fecha = models.DateField(null=True, blank=True, verbose_name="Fecha de la cita")
    hora = models.TimeField(null=True, blank=True, verbose_name="Tiempo inicial")
    hora_fin = models.TimeField(null=True, blank=True, verbose_name="Tiempo Final")
    fecha_fin = models.DateField(
        null=True,
        blank=True,
        verbose_name="Fecha fin de terapias",
        help_text="Fecha en la que dejarán de repetirse las citas"
    )

        # ✅ Nuevos campos
    DIAS_SEMANA = [
        ("lunes", "Lunes"),
        ("martes", "Martes"),
        ("miercoles", "Miércoles"),
        ("jueves", "Jueves"),
        ("viernes", "Viernes"),
        ("sabado", "Sábado"),
        ("domingo", "Domingo"),
    ]

    dias_recurrentes = models.CharField(
    max_length=100,
    blank=True,
    null=True,
    verbose_name="Días de la semana recurrentes",
    )


    motivo = models.CharField(max_length=255)
    notas = models.TextField(null=True, blank=True, verbose_name="Notas adicionales")




    pendiente = models.BooleanField(default=True, verbose_name="Pendiente")
    confirmada = models.BooleanField(default=False, verbose_name="Confirmada")
    cancelada = models.BooleanField(default=False, verbose_name="Cancelada")

    def get_duracion(self):
        if self.hora and self.hora_fin:
            # Combinar con una fecha base para poder restar
            base_date = datetime(2000, 1, 1)
            hora_inicio = datetime.combine(base_date, self.hora)
            hora_final = datetime.combine(base_date, self.hora_fin)

            if hora_final < hora_inicio:
                hora_final += timedelta(days=1)  # Para casos de paso de medianoche

            duracion = hora_final - hora_inicio
            horas, resto = divmod(duracion.seconds, 3600)
            minutos = resto // 60

            return f"{horas}h {minutos}m"
        return "—"

    def get_fecha_relativa(self):
        if not self.fecha:
            return "Sin fecha"

        hoy = date.today()
        manana = hoy + timedelta(days=1)
        diferencia = (self.fecha - hoy).days

        if self.fecha == hoy:
            return "Hoy"
        elif self.fecha == manana:
            return "Mañana"
        elif 2 <= diferencia <= 7:
            return "Esta semana"
        elif 8 <= diferencia <= 14:
            return "Próxima semana"
        elif self.fecha.month == hoy.month and self.fecha.year == hoy.year:
            return "Este mes"
        elif self.fecha.month == (hoy.month % 12) + 1 and self.fecha.year == hoy.year:
            return "Próximo mes"
        elif self.fecha.year == hoy.year + 1:
            return "Próximo año"
        elif self.fecha < hoy:
            return "Fecha pasada"
        else:
            return self.fecha.strftime("%d/%m/%Y") 

    def __str__(self):
        fecha_str = self.fecha.strftime('%d/%m/%Y') if self.fecha else 'Sin fecha'
        hora_str = self.hora.strftime('%H:%M') if self.hora else 'Sin hora'
        return f"{self.creador} → {self.profile} ({fecha_str} {hora_str})"

    def clean(self):
        super().clean()

        estados = ['pendiente', 'confirmada', 'cancelada']
        seleccionados = [estado for estado in estados if getattr(self, estado)]

        if len(seleccionados) > 1:
            raise ValidationError("Solo un estado puede estar activo a la vez: pendiente, confirmada o cancelada.")

        if len(seleccionados) == 0:
            raise ValidationError("Debe seleccionarse al menos un estado.")

        if self.fecha_fin and self.fecha and self.fecha_fin < self.fecha:
            raise ValidationError("La fecha de finalización no puede ser anterior a la fecha de inicio.")

    class Meta:
        ordering = ['-fecha', '-hora']
        verbose_name = "Cita Agendada"
        verbose_name_plural = "Citas Agendadas"


class tareas(models.Model):
    sucursal = models.ForeignKey(
        Sucursal,
        on_delete=models.CASCADE,
        related_name="sucursal6",null=True, blank=True
    )
    Insitucional_a_cargo = models.ForeignKey(
        PerfilInstitucional,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tareas_institucionales',
        verbose_name="Institución a cargo"
    )

    cita_terapeutica_asignada = models.DateField(null=True, blank=True, verbose_name="Fecha Sesion de Terapia")
    hora = models.TimeField(null=True, blank=True, verbose_name="hora de inicio")
    hora_fin = models.TimeField(null=True, blank=True, verbose_name="Hora de finalización")

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE,related_name='Asignar_perfil_de_paciente2',verbose_name="Paciente Asignado")
    fecha_envio = models.DateField(blank=True, null=True, verbose_name="Fecha de envio de tarea")
    terapeuta = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='terapeuta_asiga_tarea',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    asistire = models.BooleanField(default=False, verbose_name="¿Asistió? No/Si")
    envio_tarea = models.BooleanField(default=False, verbose_name="¿Se envía tarea? No/Si")
    titulo = models.CharField(max_length=255, blank=True, null=True, verbose_name="Título de Actividad") 
    descripcion_actividad =  HTMLField(null=True, blank=True, verbose_name="Describa la actividad a realizar")
    media_terapia =  models.FileField(upload_to='Videos/%Y/%m/%d/', blank=True, verbose_name="Video Multimedia de actividad ")
    fecha_actividad = models.DateTimeField(auto_now=True, verbose_name="Fecha de Actividad")

    actividad_realizada = models.BooleanField(default=False, verbose_name="¿Realizó la terea?")
    descripcion_tarea =  HTMLField(null=True, blank=True, verbose_name="Describa la tarea a realizar")
   
    fecha_entrega = models.DateField(blank=True, null=True, verbose_name="Fecha de entrega de tarea")
    material_adjunto =  models.FileField(upload_to='materiales/%Y/%m/%d/', blank=True, verbose_name="Material adjunto")
   
    
    tarea_realizada = models.BooleanField(default=False, verbose_name="¿Tiene Alta Terapéutica? No/Si")

    def get_duracion(self):
        if self.hora and self.hora_fin:
            base_date = datetime(2000, 1, 1)
            hora_inicio = datetime.combine(base_date, self.hora)
            hora_final = datetime.combine(base_date, self.hora_fin)

            if hora_final < hora_inicio:
                hora_final += timedelta(days=1)  # Caso de paso a medianoche

            duracion = hora_final - hora_inicio
            horas, resto = divmod(duracion.seconds, 3600)
            minutos = resto // 60

            return f"{horas}h {minutos}m"
        return "—"



    class Meta:
        ordering = ['profile__user__first_name']
        verbose_name_plural = "Tareas & Actividades Asignadas"
        verbose_name = "Paciente/ Tareas & Actividades Asignadas"

    def __str__(self):
        return f"Tareas terapéuticas de {self.profile.nombre_paciente} {self.profile.apellidos_paciente} - {self.titulo}"



class TareaComentario(models.Model):
    tarea = models.ForeignKey('tareas', on_delete=models.CASCADE, related_name='comentarios')
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    mensaje = HTMLField(null=True, blank=True, verbose_name="Comentario o actividad a realizar")
    archivo = models.FileField(upload_to='tareas_respuestas/%Y/%m/%d/', blank=True, null=True, verbose_name="Archivo adjunto")
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['fecha']
        verbose_name = "Revisar Tarea Terapeutica"
        verbose_name_plural = "Revisar Tareas"

    def __str__(self):
        return f"Corregir Tarea  {self.autor.username} - {self.tarea.titulo}"
    


class Mensaje(models.Model):
    ASUNTOS_CHOICES = [
        ('Consulta', 'Consulta'),
        ('Sugerencia', 'Sugerencia'),   
        ('Informativo', 'Informativo'),
        ('Terapéutico', 'Terapéutico'),
        ('Solicitud de pago vencido', 'Solicitud de pago vencido'),
        ('Solicitud de Certificado Médico', 'Solicitud de Certificado Médico'),
        ('Reclamo del servicio Médico', 'Reclamo del servicio Médico'),
        ('Cancelación del servicio Médico', 'Cancelación del servicio Médico'),
    ]

    sucursal = models.ForeignKey(
        Sucursal,
        on_delete=models.CASCADE,
        related_name="sucursal7",
        null=True,
        blank=True
    )

    emisor = models.ForeignKey(
    'AdministrativeProfile',  # ← ya no apunta a User
    related_name='mensajes_enviados',
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    verbose_name="Administrador emisor"
    )


    asunto = models.CharField(max_length=50, choices=ASUNTOS_CHOICES, default='Consulta')  
    cuerpo = HTMLField(null=True, blank=True, verbose_name="Cuerpo del mensaje")
    adjunto = models.FileField(
        upload_to='mensajes_adjuntos/', 
        null=True, 
        blank=True, 
        verbose_name="Archivo adjunto"
    )
    leido = models.BooleanField(default=False)
    creado = models.DateTimeField(default=timezone.now)
    fecha_envio = models.DateTimeField(auto_now_add=True)

    # 🆕 Nuevos campos para asignaciones
    receptor  = models.ForeignKey(
       'Profile',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='mensajes_perfil_paciente',
        verbose_name="Destinatario Paciente"
    )

    perfil_terapeuta = models.ForeignKey(
        'Perfil_Terapeuta',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='mensajes_perfil_terapeuta',
        verbose_name="Asignar terapeuta"
    )

    perfil_administrativo = models.ForeignKey(
        'AdministrativeProfile',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='mensajes_administrativo',
        verbose_name="Asignar administrativo"
    )

    institucion_a_cargo = models.ForeignKey(
        'PerfilInstitucional',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='mensajes_institucional',
        verbose_name="Asignar institución a cargo"
    )

    # ➕ Campo para vincular con Celery
    task_id = models.CharField(max_length=255, blank=True, null=True, help_text="ID de la tarea de Celery asociada")
    task_status = models.CharField(max_length=50, blank=True, null=True, help_text="Estado de la tarea de Celery asociada")

    class Meta:
        ordering = ['-fecha_envio']
        verbose_name_plural = "Bandeja de entrada MEDDES®"
        verbose_name = "Notificaciones de MEDDES®"

    def __str__(self):
        fecha = self.fecha_envio.strftime("%d/%m/%Y %H:%M") if self.fecha_envio else "Sin fecha"
        return f"{self.emisor} - {fecha}"

    @property
    def estado_tarea(self):
        if self.task_id:
            task_result = TaskResult.objects.filter(task_id=self.task_id).order_by('-date_done').first()
            if task_result:
                return task_result.task_state
            return "Desconocido"
        return "No asignada"


class AsistenciaTerapeuta(models.Model):
    terapeuta = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='asistencia_terapeutica',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    sucursal = models.ForeignKey(
        Sucursal,
        on_delete=models.CASCADE,
        related_name="sucursal2", null=True, blank=True
    )
    evento = models.OneToOneField(Cita, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Cita Agendada")
    hora_salida = models.TimeField(null=True, blank=True)
    asistire = models.BooleanField(default=False, verbose_name="¿Confirmo que asistiré?")
    no_asistire = models.BooleanField(default=False, verbose_name="¿Confirmo que no asistiré?")
    observaciones =  HTMLField(null=True, blank=True, verbose_name="En caso de no asistir, explique el motivo")


    class Meta:
        unique_together = ('terapeuta', 'hora_salida')
        ordering = ['-evento']

    def save(self, *args, **kwargs):
        if self.asistire and self.no_asistire:
            raise ValueError("Solo uno de los campos puede estar activo: 'asistire' o 'no_asistire'.")

        super().save(*args, **kwargs)







class ComentarioCita(models.Model):
    cita = models.ForeignKey(Cita, on_delete=models.CASCADE, related_name='comentarios')
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    texto = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentario de {self.autor.username} el {self.fecha_creacion}"


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


class BitacoraDesarrollo(models.Model):
    TIPO_SISTEMA_CHOICES = [
        ('RAPP', 'Registro administrativo/Perfil de Paciente'),
        ('RAPT', 'Registro administrativo/Perfil de Terapistas'),
        ('RAACC', 'Registro administrativo/Agenda de Citas Regulares'),
        ('RAPA', 'Registro administrativo/Prospeción Administrativa'),
        ('RAPS', 'Registro administrativo/Pago de Servicios'),
        ('RTTA', 'Registro Terapeutico/Tareas & Actividades'),
        ('RTAA', 'Registro Terapeutico/Asistencias'),
        ('SBN ', 'Bandeja de Notificaciones'),
        ('SERP', 'Visualización de ERP '),
    ]

    TIPO_TECHNOLOGIAS_CHOICES = [
        ('UX', 'Experiencia de Usuario'),
        ('UI', 'Interfase'),
        ('I+D', 'Implementación'),
        ('A', 'Automatización'),
    ]

    VERSION = [
        ('QND0301', 'QND-0.3.0.1'),
        ('QND0302', 'QND-0.3.0.2'),
        ('QND0303', 'QND-0.3.0.3'),
        ('QND0304', 'QND-0.3.0.4'),
    ]

    SQCREW = [
        ('DeV', 'Desarollo - backend'),
        ('DeV', 'Desarollo - frontend'),
        ('DeV', 'Desarollo - fullstack'),
        ('DeV', 'Desarollo - QA'),
        ('DeV', 'Desarollo - UI/UX'),
        ('DeV', 'Desarollo - I+D'),
        ('ProD', 'Producción -backend'),
        ('ProD', 'Producción - frontend'),
        ('ProD', 'Producción - fullstack'),
        ('ProD', 'Producción - QA'),
        ('ProD', 'Producción - UI/UX'),
        ('ProD', 'Producción - I+D'),
        ('StG', 'Soporte - backend'),
        ('StG', 'Soporte - frontend'),
        ('StG', 'Soporte - fullstack'),
        ('StG', 'Soporte - QA'),
        ('StG', 'Soporte - UI/UX'),
        ('StG', 'Soporte - I+D'),
        ('StG', 'Soporte - Producción'),
        ('DA', 'Data Analytics'),
    ]

    INCHARGE = [
        ('DeV', 'Mauricio Silva'),
        ('Prod', 'Andres Espinoza'),
        ('Front', 'Virginia Lasta'),
    ]

    STATE = [
        ('Revisión', 'Revisión'),
        ('Desarollo', 'Desarollo'),
        ('Pruebas', 'Pruebas'),
        ('Producción', 'Producción'),
        ('Aprobado', 'Aprobado'),
    ]

    version_relacionada = models.CharField(blank=True, null=True, max_length=200, choices=VERSION, verbose_name="Versión", default="QND-0.3.0.1")
    fecha = models.DateTimeField(auto_now_add=True)
    fecha_entrega = models.DateField(blank=True, null=True)  # nuevo campo automático
    incarge = models.CharField(blank=True, null=True,max_length=200, choices=INCHARGE)
    SmartQuail_Tech = models.CharField(max_length=200, choices=SQCREW,null=True, blank=True)
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tipo_cambio = models.CharField(max_length=200, choices=TIPO_SISTEMA_CHOICES)
    tipo_tecnologia = models.CharField(max_length=200, choices=TIPO_TECHNOLOGIAS_CHOICES)
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    progreso = models.PositiveIntegerField(default=0) 
    estado =  models.CharField(blank=True, null=True, max_length=200, choices=STATE, verbose_name="ESTADO",default="Revisión")

    minutos_empleados = models.PositiveIntegerField(default=0, verbose_name="Minutos Empleados")
    minutos_restantes = models.PositiveIntegerField(default=4320, editable=False, verbose_name="Minutos Restantes")

    class Meta:
        verbose_name = "Entrada de Bitácora"
        verbose_name_plural = "Bitácora de Desarrollo QND.0.3.0.2"
        ordering = ['-fecha']

    def __str__(self):
        return f"[{self.fecha.strftime('%Y-%m-%d')}] {self.titulo} - {self.autor.username}"

    def save(self, *args, **kwargs):
        if not self.fecha_entrega:
            self.fecha_entrega = (timezone.now() + timedelta(days=5)).date()

        # Calcula los minutos restantes antes de guardar
        TOTAL_MINUTOS = 4320
        self.minutos_restantes = max(TOTAL_MINUTOS - self.minutos_empleados, 0)

        super().save(*args, **kwargs)








# Cliente simplificado
class Cliente(models.Model):
    nombre = models.ForeignKey(
        'AdministrativeProfile',
        on_delete=models.CASCADE,
        related_name='clientes',
        verbose_name="Elija su usuario Administrativo en el sistema Sistema MEDDES™")


    class Meta:
        verbose_name = "ticket de soporte - SmartQuail, Inc."
        verbose_name_plural = " ticket de soporte - SmartQuail, Inc"
    

    def __str__(self):
        return f"{self.nombre} ({self.empresa})" if self.empresa else self.nombre


# Problemas frecuentes conocidos
class ProblemaFrecuente(models.Model):
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE, related_name='problemas_frecuentes')
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    solucion_recomendada = models.TextField()
    categoria = models.CharField(max_length=100, choices=[
        ('conexion', 'Problemas de conexión'),
        ('rendimiento', 'Rendimiento lento'),
        ('seguridad', 'Incidentes de seguridad'),
        ('backup', 'Errores de backup'),
        ('acceso', 'Problemas de acceso'),
        ('otros', 'Otros'),
    ])

    def __str__(self):
        return self.titulo


# Preguntas frecuentes
class PreguntaFrecuente(models.Model):
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE, related_name='preguntas_frecuentes')
    pregunta = models.CharField(max_length=255)
    respuesta = models.TextField()
    categoria = models.CharField(max_length=100, choices=[
        ('cuenta', 'Cuenta y acceso'),
        ('facturacion', 'Facturación'),
        ('seguridad', 'Seguridad'),
        ('soporte', 'Soporte técnico'),
        ('general', 'General'),
    ])

    def __str__(self):
        return self.pregunta


# Ticket de soporte actualizado
class TicketSoporte(models.Model):
    
    ESTADO_CHOICES = [
        ('abierto', 'Abierto'),
        ('en_proceso', 'En proceso'),
        ('resuelto', 'Resuelto'),
        ('cerrado', 'Cerrado'),
    ]

    PRIORIDAD_CHOICES = [
        ('baja', 'Baja'),
        ('media', 'Media'),
        ('alta', 'Alta'),
        ('critica', 'Crítica'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    problema_relacionado = models.ForeignKey(ProblemaFrecuente, null=True, blank=True, on_delete=models.SET_NULL)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='abierto')
    prioridad = models.CharField(max_length=10, choices=PRIORIDAD_CHOICES, default='media')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"[#{self.id}] {self.titulo}"
