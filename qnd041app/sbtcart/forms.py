from django import forms


PRODUCT_QUANTITY_CHOICES = [(i, f"{i} mes(es)") for i in range(1, 12)]  # Ejemplo de opciones de cantidad

class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(
        choices=PRODUCT_QUANTITY_CHOICES,
        coerce=int,
        help_text="Elija los meses de suscripción",
        label="Elija la cantidad de meses de su suscripción"  # Directamente el label aquí
    )
    update = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.HiddenInput
    )
    
    # Si necesitas inicializar valores predeterminados o validar algo adicional, puedes hacerlo aquí
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Puedes establecer un valor inicial predeterminado, si es necesario
        self.fields['quantity'].initial = 3  # Esto es opcional y establece un valor predeterminado en 1