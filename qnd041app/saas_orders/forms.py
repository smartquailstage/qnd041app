from django import forms
from .models import SaaSOrder


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = SaaSOrder
        fields = ['ruc', 'razon_social', 'sector', 'telefono']

    # Agregar clases de Bootstrap a los campos
    ruc = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    razon_social = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    sector = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    telefono = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
