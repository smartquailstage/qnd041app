from django import forms

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(3, 13)]

class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(
        choices=PRODUCT_QUANTITY_CHOICES,
        coerce=int,
        initial=3,  # Establece el valor por defecto a 3
     
    )
    update = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.HiddenInput
    )