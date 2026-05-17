from django import forms
from django.utils.translation import gettext_lazy as _


class CouponApplyForm(forms.Form):
    code = forms.CharField(label=_('Coupon'))


# forms.py

from django import forms
from .models import Coupon


class CouponRequestForm(forms.ModelForm):

    class Meta:
        model = Coupon

        fields = [
            'ingresos_anuales',
            'presupuesto_real',
            'descripcion_valor_agregado',
            'credito',
        ]

        widgets = {

           'ingresos_anuales': forms.TextInput(
    attrs={
        'class': 'form-control',
        'placeholder': 'Escriba un valor aproximado de ingresos anuales. Ej: 150000.00'
    }
),

'presupuesto_real': forms.TextInput(
    attrs={
        'class': 'form-control',
        'placeholder': 'Escriba un valor presupuesto disponible parar inverión en tecnología. Ej: 25000.00'
    }
),

            'descripcion_valor_agregado': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 5,
                    'placeholder': 'Describa el valor agregado de su proyecto'
                }
            ),
        }

        labels = {
            'ingresos_anuales': 'Ingresos anuales',
            'presupuesto_real': 'Presupuesto real disponible',
            'descripcion_valor_agregado': 'Valor agregado del proyecto',
            'credito': 'Elegir tipo de credito, si aplica.' 
        }