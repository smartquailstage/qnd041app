from django import forms
from django.contrib.auth.models import User, Group
from .models import Profile
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
#from django.contrib.admin.widgets import AdminDateWidget
from django.forms.fields import DateField
from django.forms import DateInput
from .models import Mensaje, Cita ,TareaComentario
from serviceapp.models import ServicioTerapeutico
from ckeditor.widgets import CKEditorWidget
from django.forms.models import inlineformset_factory
from .models import AsistenciaTerapeuta, prospecion_administrativa, DocenteCapacitado, Perfil_Terapeuta, ValoracionTerapia, AdministrativeProfile
from bootstrap_datepicker_plus.widgets import DatePickerInput
from django import forms
from .widgets import CustomDatePickerWidget
from .widgets import CustomTimePickerWidget, CustomDateTimePickerWidget
from django.utils.timezone import localtime, is_naive, make_aware
from datetime import date, datetime




class AdministrativeProfileForm(forms.ModelForm):
    class Meta:
        model = AdministrativeProfile
        fields = '__all__'
        widgets = {
            'date_of_birth': CustomDatePickerWidget(attrs={'class': 'form-control'}),
            'date_joined': CustomDatePickerWidget(attrs={'class': 'form-control'}),
        }


class LoginForm(forms.Form):
    email = forms.EmailField(label="Correo electrónico")
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")

    

class MensajeForm(forms.ModelForm):
    class Meta:
        model = Mensaje
        fields = ['cuerpo']
        widgets = {
            'cuerpo': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Escribe tu mensaje aquí...'
            }),
        }

class LeidoForm(forms.ModelForm):
    class Meta:
        model = Mensaje
        fields = ['leido']
        widgets = {
            'leido': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class MarcarLeidoForm(forms.ModelForm):
    class Meta:
        model = Mensaje
        fields = []

DIAS_SEMANA = [
    ("lunes", "Lunes"),
    ("martes", "Martes"),
    ("miercoles", "Miércoles"),
    ("jueves", "Jueves"),
    ("viernes", "Viernes"),
    ("sabado", "Sábado"),
    ("domingo", "Domingo"),
]

class CitaForm(forms.ModelForm):
    dias_recurrentes = forms.MultipleChoiceField(
        choices=DIAS_SEMANA,
        required=False,
        widget=forms.CheckboxSelectMultiple(),
        label="Días de la semana (recurrentes)"
    )

    class Meta:
        model = Cita
        # Aquí pones todos los campos que quieras mostrar (o '__all__' para todos)
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.dias_recurrentes:
            self.initial["dias_recurrentes"] = self.instance.dias_recurrentes.split(",")

    def clean_dias_recurrentes(self):
        return ",".join(self.cleaned_data.get("dias_recurrentes", []))

    def save(self, commit=True, creador=None, destinatario=None):
        cita = super().save(commit=False)

        if creador:
            cita.creador = creador
        if destinatario:
            cita.destinatario = destinatario

        # Estados por defecto
        cita.pendiente = True
        cita.confirmada = False
        cita.cancelada = False

        if commit:
            cita.save()
        return cita


class CitaPacienteForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['fecha', 'hora', 'notas']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hora': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'notas': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

        
class TareaComentarioForm(forms.ModelForm):
    class Meta:
        model = TareaComentario
        fields = ['mensaje', 'archivo']
        widgets = {
            'mensaje': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'archivo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class ServicioTerapeuticoForm(forms.ModelForm):
    TIPO_SERVICIO = [
        ('TERAPIA DE LENGUAJE', 'Terapia de Lenguaje'),
        ('ESTIMULACIÓN COGNITIVA', 'Estimulación Cognitiva'),
        ('PSICOLOGÍA', 'Psicología'),
        ('ESTIMULACIÓN TEMPRANA', 'Estimulación Temprana'),
        ('VALORACIÓN TERAPEUTICA', 'Valoración Terapeutica'),
    ]

    tipos = forms.MultipleChoiceField(
        choices=TIPO_SERVICIO,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Tipo de servicio"
    )

    class Meta:
        model = ServicioTerapeutico
        fields = '__all__'

    def clean_tipos(self):
        return self.cleaned_data['tipos']


DocenteCapacitadoFormSet = inlineformset_factory(
    prospecion_administrativa,
    DocenteCapacitado,
    fields=[
        'fecha_capacitacion', 'area_capacitacion', 'tema',
        'nombres', 'apellidos', 'correo', 'cedula', 'telefono'
    ],
    extra=1,
    can_delete=True,
    max_num=100
)


class ProspecionAdministrativaForm(forms.ModelForm):
    class Meta:
        model = prospecion_administrativa
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.docentes_formset = DocenteCapacitadoFormSet(
            instance=self.instance,
            data=kwargs.get('data') if kwargs.get('data') else None
        )

    def is_valid(self):
        return super().is_valid() and self.docentes_formset.is_valid()

    def save(self, commit=True):
        instance = super().save(commit)
        self.docentes_formset.instance = instance
        self.docentes_formset.save()
        return instance



class PerfilTerapeutaForm(forms.ModelForm):
    class Meta:
        model = Perfil_Terapeuta
        fields = '__all__'
        widgets = {
            'fecha_nacimiento': CustomDatePickerWidget(),
        }



class PerfilTerapeutaAdminForm(forms.ModelForm):
    TIPO_SERVICIO = Perfil_Terapeuta.TIPO_SERVICIO

    tipos = forms.MultipleChoiceField(
        choices=TIPO_SERVICIO,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Tipo de servicio (múltiples opciones)",
        help_text="Selecciona uno o más tipos"
    )

    class Meta:
        model = Perfil_Terapeuta
        fields = [
            'user', 'especialidad', 'nombres_completos', 'sexo', 'fecha_nacimiento', 'cedula',
            'fecha_ingreso', 'sucursal', 'telefono',
            'titulo_universitario', 'antecedentes_penales', 'certificados',
            'banco', 'tipo_cuenta', 'numero_cuenta',
            'servicio_domicilio', 'pago_por_hora',
            'servicio_institucion', 'pago_por_hora_institucion',
            'servicio_consulta', 'pago_por_hora_consulta',
            'tipos', 'activo'
        ]
        widgets = {
            'fecha_nacimiento': CustomDatePickerWidget(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.initial['tipos'] = self.instance.tipos

    def clean_tipos(self):
        return self.cleaned_data['tipos']

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.tipos = self.cleaned_data.get('tipos', [])
        if commit:
            instance.save()
            self.save_m2m()
        return instance


        
class PerfilPacientesForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        widgets = {
            'fecha_nacimiento': CustomDatePickerWidget(),
        }


class ValoracionTerapiaAdminForm(forms.ModelForm):
    class Meta:
        model = ValoracionTerapia
        fields = '__all__'
        widgets = {
            'fecha_valoracion': CustomDatePickerWidget(attrs={
                'class': 'form-control', 'placeholder': 'dd/mm/aaaa'
            }),
            'fecha_nacimiento': CustomDatePickerWidget(attrs={
                'class': 'form-control', 'placeholder': 'dd/mm/aaaa'
            }),
            'fecha_asesoria': CustomDatePickerWidget(attrs={
                'class': 'form-control', 'placeholder': 'dd/mm/aaaa'
            }),
        }


class CitaAdminForm(forms.ModelForm):
    fecha_input = forms.DateField(
        label="Fecha de la cita",
        widget=CustomDatePickerWidget(attrs={'class': 'form-control'}),
        required=False
    )
    hora_input = forms.TimeField(
        label="Hora de la cita",
        widget=CustomTimePickerWidget(attrs={'class': 'form-control'}),
        required=False
    )

    class Meta:
        model = Cita
        fields = [  # No incluimos `fecha` directamente
            'destinatario','fecha','hora' ,'sucursal', 'tipo_cita', 'motivo', 'notas',
            'profile', 'profile_terapeuta',
            'pendiente', 'confirmada', 'cancelada'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.fecha:
            fecha_valor = self.instance.fecha
            if isinstance(fecha_valor, datetime):
                self.fields['fecha_input'].initial = fecha_valor.date()
                self.fields['hora_input'].initial = fecha_valor.time()
            elif isinstance(fecha_valor, date):
                self.fields['fecha_input'].initial = fecha_valor
                self.fields['hora_input'].initial = None

    def clean(self):
        cleaned_data = super().clean()
        fecha = cleaned_data.get('fecha_input')
        hora = cleaned_data.get('hora_input')

        if fecha and hora:
            cleaned_data['fecha'] = datetime.combine(fecha, hora)
            
        else:
            cleaned_data['fecha'] = None

        return cleaned_data

    def save(self, commit=True):
        self.instance.fecha = self.cleaned_data.get('fecha')
        return super().save(commit)


class ProfileAdminForm(forms.ModelForm):
    TIPO_SERVICIO = [
        ('TERAPIA DE LENGUAJE', 'Terapia de Lenguaje'),
        ('ESTIMULACIÓN COGNITIVA', 'Estimulación Cognitiva'),
        ('PSICOLOGÍA', 'Psicología'),
        ('ESTIMULACIÓN TEMPRANA', 'Estimulación Temprana'),
        ('VALORACIÓN', 'Valoración'),
        ('TERAPIA OCUPACIONAL', 'Terápia Ocupacional'),
    ]

    tipos = forms.MultipleChoiceField(
        choices=TIPO_SERVICIO,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Servicios Terapéuticos",
        help_text="Seleccionar uno o más servicios"
    )

    class Meta:
        model = Profile
        fields = '__all__'
        widgets = {
            'fecha_nacimiento': CustomDatePickerWidget(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.initial['tipos'] = self.instance.tipos or []

    def clean_tipos(self):
        return self.cleaned_data['tipos']

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.tipos = self.cleaned_data.get('tipos', [])
        if commit:
            instance.save()
            self.save_m2m()
        return instance



class AsistenciaTerapeutaAdminForm(forms.ModelForm):
    class Meta:
        model = AsistenciaTerapeuta
        fields = '__all__'
        widgets = {
            'hora_salida': CustomTimePickerWidget(
                attrs={'class': 'form-control', 'placeholder': 'HH:MM'}
            ),
        }


class AutorizacionForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['adjunto_autorizacion']
        labels = {'adjunto_autorizacion': 'Archivo de autorización'}