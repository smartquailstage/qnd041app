from django import forms
from .models import SaaSOrder
from localflavor.us.forms import USZipCodeField


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = SaaSOrder
        fields = ['ruc', 'razon_social', 'sector','telefono']