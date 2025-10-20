# forms.py
from django import forms
from .models import BusinessSystemProject, BusinessProcess, BusinessAutomation, BusinessIntelligent, QATest, CloudResource
from usuarios.models import SmartQuailCrew


from django.forms import modelformset_factory, inlineformset_factory


class BusinessSystemProjectForm(forms.ModelForm):
    class Meta:
        model = BusinessSystemProject
        fields = ['name', 'description', 'business_sector','product']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }


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