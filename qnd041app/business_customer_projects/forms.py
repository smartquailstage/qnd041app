# forms.py
from django import forms
from .models import BusinessSystemProject, BusinessProcess, BusinessAutomation, BusinessIntelligent, QATest, CloudResource
from usuarios.models import SmartQuailCrew


from django.forms import modelformset_factory, inlineformset_factory


from django import forms
from .models import BusinessSystemProject
from saas_shop.models import Product


from saas_orders.models import SaaSOrder

class ContractUploadForm(forms.ModelForm):
    class Meta:
        model = SaaSOrder
        fields = ['signed_contract']

    def clean_signed_contract(self):
        file = self.cleaned_data['signed_contract']

        if file.size > 5 * 1024 * 1024:
            raise forms.ValidationError("El archivo no puede superar 5MB")

        if not file.name.lower().endswith(('.pdf', '.png', '.jpg', '.jpeg')):
            raise forms.ValidationError("Formato no permitido")

        return file



class BusinessSystemProjectForm(forms.ModelForm):

    class Meta:
        model = BusinessSystemProject
        fields = [
            'product',
            'is_domain_configured',
            'domain_name',
            'logo_rectangular',
            'logo_cuadrado',
        ]

        widgets = {

            'product': forms.Select(attrs={'class': 'form-control'}),

            'is_domain_configured': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),

            'domain_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ejemplo.midominio.com',
            }),

            'logo_rectangular': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
            }),

            'logo_cuadrado': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
            }),
        }

        help_texts = {
            'name': 'Asigne un nombre representativo a su proyecto IT Cloud.',
            'is_domain_configured': 'Marque esta opción si desea configurar un dominio privado asociado al proyecto.',
            'domain_name': 'Ingrese el dominio privado que desea usar (solo si selecciona la opción anterior).',
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)

        # Filtrar productos comprados por el usuario
        if user:
            self.fields['product'].queryset = Product.objects.filter(
                saas_order_items__order__user=user
            ).distinct()

        # Hacer que domain_name sea opcional por defecto
        self.fields['domain_name'].required = False

    def clean(self):
        cleaned_data = super().clean()

        wants_domain = cleaned_data.get('is_domain_configured')
        domain_name = cleaned_data.get('domain_name')

        # Validar que si marca el checkbox, debe ingresar un dominio
        if wants_domain and not domain_name:
            self.add_error('domain_name', "Debe ingresar el nombre del dominio privado.")

        return cleaned_data




class BusinessProcessForm(forms.ModelForm):
    class Meta:
        model = BusinessProcess
        fields = ['name', 'description', 'progress', 'has_automation', 'automation_description',
                  'has_ai', 'ai_model_description', 'assigned_developer', 'start_date', 'delivery_date',
                  'approved_by_client', 'process_type', 'technology_type', 'process_class', 'final_url']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'automation_description': forms.Textarea(attrs={'rows': 4}),
            'ai_model_description': forms.Textarea(attrs={'rows': 4}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'delivery_date': forms.DateInput(attrs={'type': 'date'}),
        }

class BusinessAutomationForm(forms.ModelForm):
    class Meta:
        model = BusinessAutomation
        fields = ['name', 'description', 'progress', 'automation_type', 'assigned_developer',
                  'start_date', 'delivery_date', 'approved_by_client', 'final_url']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'delivery_date': forms.DateInput(attrs={'type': 'date'}),
        }

class BusinessIntelligentForm(forms.ModelForm):
    class Meta:
        model = BusinessIntelligent
        fields = ['name', 'description', 'progress', 'ai_type', 'requires_gpu', 'model_accuracy', 
                  'decision_maps', 'technical_notes', 'assigned_developer', 'start_date', 'delivery_date', 
                  'approved_by_client', 'final_url']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'decision_maps': forms.Textarea(attrs={'rows': 4}),
            'technical_notes': forms.Textarea(attrs={'rows': 4}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'delivery_date': forms.DateInput(attrs={'type': 'date'}),
        }

class QATestForm(forms.ModelForm):
    class Meta:
        model = QATest
        fields = ['test_case', 'description', 'result', 'executed_by']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class CloudResourceForm(forms.ModelForm):
    class Meta:
        model = CloudResource
        fields = ['resource_type', 'provider', 'resource_name', 'monthly_cost_usd', 
                  'monitoring_tool', 'monitoring_status', 'alert_summary']
        widgets = {
            'monthly_cost_usd': forms.NumberInput(attrs={'step': '0.01'}),
        }


class ProjectWithComponentsForm(forms.Form):
    project = BusinessSystemProjectForm()
    processes = inlineformset_factory(BusinessSystemProject, BusinessProcess, form=BusinessProcessForm, extra=1)
    automations = inlineformset_factory(BusinessSystemProject, BusinessAutomation, form=BusinessAutomationForm, extra=1)
    intelligents = inlineformset_factory(BusinessSystemProject, BusinessIntelligent, form=BusinessIntelligentForm, extra=1)
    tests = inlineformset_factory(BusinessProcess, QATest, form=QATestForm, extra=1)
    resources = inlineformset_factory(BusinessSystemProject, CloudResource, form=CloudResourceForm, extra=1)




from django import forms
from .models import ComentarioNoticia

class ComentarioNoticiaForm(forms.ModelForm):
    class Meta:
        model = ComentarioNoticia
        fields = ['comentario']
        widgets = {
            'comentario': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Escribe tu comentario...'
            })
        }



from django import forms
from .models import SupportTicket


class SupportTicketForm(forms.ModelForm):
    class Meta:
        model = SupportTicket
        fields = [
            'consultation_type',
            'area',
            'question',
            'title',
            'description',
            'scheduled_datetime',
        ]
        widgets = {
            'scheduled_datetime': forms.DateTimeInput(
                attrs={'type': 'datetime-local'}
            ),
            'description': forms.Textarea(attrs={'rows': 4}),
        }
