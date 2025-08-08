from django import forms
from .models import Estimacion, Servicio

class EstimacionForm(forms.Form):
    servicio = forms.ModelChoiceField(
        queryset=Servicio.objects.all(),
        label="Servicio",
        help_text="Selecciona un servicio",
        widget=forms.Select(attrs={"class": "form-control"})
    )
    usuarios_estimados = forms.IntegerField(
        min_value=1,
        label="Usuarios estimados",
        widget=forms.NumberInput(attrs={"class": "form-control"})
    )
    tipo_uso = forms.ChoiceField(
        choices=[
            ('transaccional', 'Transaccional'),
            ('analitico', 'Analítico'),
            ('mixto', 'Mixto'),
        ],
        label="Tipo de uso",
        widget=forms.Select(attrs={"class": "form-control"})
    )
    proveedor = forms.ChoiceField(
        choices=[
            ('aws', 'AWS'),
            ('azure', 'Azure'),
            ('gcp', 'GCP'),
        ],
        label="Proveedor",
        widget=forms.Select(attrs={"class": "form-control"})
    )