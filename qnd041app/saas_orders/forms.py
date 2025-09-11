from django import forms
from .models import SaaSOrder


from django import forms
from .models import SaaSOrder

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = SaaSOrder
        fields = ['ruc', 'razon_social', 'sector', 'telefono']

    # Agregar clases de Bootstrap a los campos
    ruc = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    razon_social = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    # Cambiar el widget de sector a Select
    sector = forms.ChoiceField(choices=SaaSOrder.SECTORES, widget=forms.Select(attrs={'class': 'form-select'}))

    telefono = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
