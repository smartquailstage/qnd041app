from django import forms
from .models import SaaSOrder


from django import forms
from .models import SaaSOrder



class AcceptTermsForm(forms.Form):
    terms_accepted = forms.BooleanField(
        required=True,
        label="He leído y acepto los términos y condiciones",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = SaaSOrder
        fields = ['terms_accepted']


class OrderCreateForm(forms.ModelForm):

    class Meta:
        model = SaaSOrder
        fields = ['ruc', 'razon_social']

    # Agregar clases de Bootstrap a los campos
    ruc = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    razon_social = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))





