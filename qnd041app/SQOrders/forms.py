from django import forms
from .models import PRODUCT_CHOICES
from .models import INFRA_CHOICES

class InfrastructureForm(forms.Form):
    infra_type = forms.ChoiceField(choices=INFRA_CHOICES, label="Tipo de Infraestructura")
    cpu_cores = forms.IntegerField(label="Cores de CPU", min_value=1)
    ram_gb = forms.IntegerField(label="Memoria RAM (GB)", min_value=1)
    storage_gb = forms.IntegerField(label="Almacenamiento (GB)", min_value=10)
    bandwidth_mbps = forms.IntegerField(label="Ancho de Banda (Mbps)", min_value=10)
    

class CostCalculatorForm(forms.Form):
    product = forms.ChoiceField(choices=PRODUCT_CHOICES, label="Producto")
    include_rd = forms.BooleanField(label="I+D", required=False)
    include_automation = forms.BooleanField(label="Automatización", required=False)
    include_ai = forms.BooleanField(label="Inteligencia Artificial", required=False)
    num_processes = forms.IntegerField(label="N° de procesos", min_value=1, initial=1)
    data_volume = forms.IntegerField(label="Volumen de datos (MB)", min_value=0, initial=0)
    complexity = forms.IntegerField(label="Complejidad (1-5)", min_value=1, max_value=5, initial=1)
