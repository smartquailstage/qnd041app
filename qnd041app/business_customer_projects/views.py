from django.views.generic.detail import DetailView
from .models import BusinessSystemProject, BusinessAutomation, BusinessIntelligent

class BusinessSystemProjectDetailView(DetailView):
    model = BusinessSystemProject
    template_name = "business/project_detail.html"
    context_object_name = "project"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.get_object()

        # Obtener procesos
        context["processes"] = project.processes.all()

        # ✅ Obtener automatizaciones e IA usando related_name
        context["automations"] = project.automations.all()
        context["intelligents"] = project.intelligents.all()

        # Recursos cloud
        context["cloud_resources"] = project.cloud_resources.all()

        # Pestañas condicionales
        context["has_automation"] = context["processes"].filter(has_automation=True).exists() or context["automations"].exists()
        context["has_ai"] = context["processes"].filter(has_ai=True).exists() or context["intelligents"].exists()

        # Personal a cargo
        context["staff"] = project.crew_members.all()

        return context

from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from .forms import ProjectWithComponentsForm

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import (BusinessSystemProjectForm, BusinessProcessForm, BusinessAutomationForm, 
                    BusinessIntelligentForm, QATestForm, CloudResourceForm, ProjectWithComponentsForm)
from .models import BusinessSystemProject, BusinessProcess, BusinessAutomation, BusinessIntelligent
from django.forms import modelformset_factory

from django.contrib.auth.decorators import login_required

@login_required
def create_project(request):
    if request.method == 'POST':
        # Incluimos el usuario logueado en el formulario
        project_form = BusinessSystemProjectForm(request.POST)
        if project_form.is_valid():
            project = project_form.save(commit=False)
            project.user = request.user  # Asignamos el usuario logueado
            project.save()  # Guardamos el proyecto
            return redirect('business_customer_projects:processes', project_id=project.id)  # Redirigimos a la URL de los procesos
    else:
        project_form = BusinessSystemProjectForm()

    return render(request, 'create_project.html', {'form': project_form})



def create_process(request, project_id):
    projects = BusinessSystemProject.objects.filter(user=request.user)
    project = BusinessSystemProject.objects.get(id=project_id)
    if request.method == 'POST':
        process_form = BusinessProcessForm(request.POST)
        if process_form.is_valid():
            process = process_form.save(commit=False)
            process.project = project
            process.save()
            return redirect('automation', project_id=project.id)  # Redirige a automatización
    else:
        process_form = BusinessProcessForm()
    return render(request, 'create_process.html', {'form': process_form, 'project': project, 'projects': projects})

def create_automation(request, project_id):
    project = BusinessSystemProject.objects.get(id=project_id)
    if request.method == 'POST':
        automation_form = BusinessAutomationForm(request.POST)
        if automation_form.is_valid():
            automation = automation_form.save(commit=False)
            automation.project = project
            automation.save()
            return redirect('ai', project_id=project.id)  # Redirige a la sección de AI
    else:
        automation_form = BusinessAutomationForm()
    return render(request, 'create_automation.html', {'form': automation_form, 'project': project})

def create_ai(request, project_id):
    project = BusinessSystemProject.objects.get(id=project_id)
    if request.method == 'POST':
        ai_form = BusinessIntelligentForm(request.POST)
        if ai_form.is_valid():
            ai = ai_form.save(commit=False)
            ai.project = project
            ai.save()
            return redirect('success')  # Redirige a la página de éxito (o a cualquier página que prefieras)
    else:
        ai_form = BusinessIntelligentForm()
    return render(request, 'create_ai.html', {'form': ai_form, 'project': project})

def create_qa_test(request, process_id):
    process = BusinessProcess.objects.get(id=process_id)
    if request.method == 'POST':
        qa_test_form = QATestForm(request.POST)
        if qa_test_form.is_valid():
            qa_test = qa_test_form.save(commit=False)
            qa_test.process = process
            qa_test.save()
            return redirect('process_detail', process_id=process.id)  # Redirige al detalle del proceso
    else:
        qa_test_form = QATestForm()
    return render(request, 'create_qa_test.html', {'form': qa_test_form, 'process': process})

def create_cloud_resource(request, project_id):
    project = BusinessSystemProject.objects.get(id=project_id)
    if request.method == 'POST':
        resource_form = CloudResourceForm(request.POST)
        if resource_form.is_valid():
            resource = resource_form.save(commit=False)
            resource.project = project
            resource.save()
            return redirect('project_detail', project_id=project.id)  # Redirige al detalle del proyecto
    else:
        resource_form = CloudResourceForm()
    return render(request, 'create_cloud_resource.html', {'form': resource_form, 'project': project})





