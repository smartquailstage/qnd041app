from django import forms
from .models import ServicesOrder



class AcceptTermsForm(forms.Form):
    terms_accepted = forms.BooleanField(
        required=True,
        label="He leído y acepto los términos y condiciones",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = ServicesOrder
        fields = ['terms_accepted']


class OrderCreateForm(forms.ModelForm):

    class Meta:
        model = ServicesOrder
        fields = ['ruc', 'razon_social', 'sector', 'telefono']

    # Agregar clases de Bootstrap a los campos
    ruc = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    razon_social = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    # Cambiar el widget de sector a Select
    sector = forms.ChoiceField(choices=SaaSOrder.SECTORES, widget=forms.Select(attrs={'class': 'form-select'}))

    telefono = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))


