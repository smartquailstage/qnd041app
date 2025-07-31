from django import forms
from .models import Order,BankTransfer


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'phonenumber'  , 'address',
                   'city','business_name','RUC','accept_terms_and_conditions']
        labels = {
            'RUC': 'Registro único de contrinbuyente, R.U.C' ,
        }



class PaymentMethodForm(forms.Form):
    # Usamos las opciones de PAYMENT_CHOICES del modelo Order
    PAYMENT_METHOD_CHOICES = Order.PAYMENT_CHOICES

    payment_method = forms.ChoiceField(
        choices=PAYMENT_METHOD_CHOICES,
        widget=forms.RadioSelect,  # Usamos RadioSelect para mostrar las opciones como botones de radio
        required=True  # Si deseas que sea obligatorio
    )

    class Meta:
        model = Order
        fields = ['payment_method']
        





class BankTransferForm(forms.ModelForm):
    class Meta:
        model = BankTransfer
        fields = ['bank', 'bank_id', 'accept_terms_and_conditions']  # Añadir el campo 'accept_terms_and_conditions'
        
        # Labels y help_texts personalizados
        labels = {
            'bank': 'Nombre de Institución financiera desde donde se realiza el pago',
            'bank_id': 'ID de operación bancaria realizada',
            'accept_terms_and_conditions': 'Acepto los términos y condiciones del contrato',  # Descripción del nuevo campo
        }
        help_texts = {
            'bank': 'Selecciona la institución financiera desde donde realizaste la transferencia.',
            'bank_id': 'Proporciona el ID de la operación bancaria que se realizó.',
            'accept_terms_and_conditions': 'Debes aceptar los términos y condiciones para completar el proceso de transferencia.',  # Ayuda adicional para el campo
        }

        # Si deseas agregar validaciones adicionales, puedes hacerlo en el formulario también.

     