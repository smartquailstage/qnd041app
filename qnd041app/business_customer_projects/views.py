from django.views.generic.detail import DetailView
from .models import BusinessSystemProject, BusinessAutomation, BusinessIntelligent

# views.py
import json
from datetime import datetime
from dateutil.relativedelta import relativedelta
from collections import defaultdict
from datetime import datetime
from dateutil.relativedelta import relativedelta
import json
from django.db.models import Avg


from django.views.generic import DetailView
from django.db.models import Avg
from .models import BusinessSystemProject

class BusinessSystemProjectDetailView(DetailView):
    model = BusinessSystemProject
    template_name = "business/project_detail.html"
    context_object_name = "project"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.get_object()

        # Todos los procesos del proyecto
        processes = project.processes.all()
        context["processes"] = processes

        # Estadísticas de procesos
        total_processes = processes.count()
        completed_processes = processes.filter(progress=100).count()
        in_progress_processes = total_processes - completed_processes
        average_progress = processes.aggregate(avg=Avg("progress"))["avg"] or 0

        # Procesos filtrados por progreso para usar en el template
        processes_completed = processes.filter(progress=100)
        processes_in_progress = processes.exclude(progress=100)

        context.update({
            "total_processes": total_processes,
            "completed_processes": completed_processes,
            "in_progress_processes": in_progress_processes,
            "average_progress": round(average_progress),
            "processes_completed": processes_completed,
            "processes_in_progress": processes_in_progress,
        })

        # Otros contextos existentes
        context["has_automation"] = project.has_automation
        context["has_ai"] = project.has_ai
        context["is_active"] = project.is_active
        context["staff"] = project.crew_members.all()
        context["cloud_resources"] = project.cloud_resources.all()

        return context




from django.views.generic import ListView
from django.db.models import Avg
from .models import BusinessProcess

from django.db.models import Avg, Sum
from django.contrib.auth import get_user_model
from django.views.generic import ListView
from .models import BusinessProcess

from django.db.models import Avg, Sum

class BusinessProcessListView(ListView):
    model = BusinessProcess
    template_name = "business/I_D.html"
    context_object_name = "processes"
    paginate_by = 20

    def get_queryset(self):
        project_id = self.request.GET.get("project")
        if project_id:
            return BusinessProcess.objects.filter(project_id=project_id)
        return BusinessProcess.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()

        # Estadísticas generales
        total = queryset.count()
        completed = queryset.filter(progress=100).count()
        in_progress = queryset.filter(progress__lt=100).count()
        average_progress = queryset.aggregate(avg=Avg("progress"))["avg"] or 0

        # Total memoria y CPU consumidos
        total_memory_used = queryset.aggregate(total_mem=Sum('memory_consumption'))['total_mem'] or 0
        total_cpu_used = queryset.aggregate(total_cpu=Sum('cpu_consumption'))['total_cpu'] or 0

        # Limites totales de memoria y CPU (usamos el máximo de los procesos para ejemplo)
        total_memory_available = queryset.aggregate(total_mem_avail=Sum('total_memory_available'))['total_mem_avail'] or 1
        total_cpu_available = queryset.aggregate(total_cpu_avail=Sum('total_cpu_available'))['total_cpu_avail'] or 1

        # Porcentaje de uso
        memory_percent = round((total_memory_used / total_memory_available) * 100, 2)
        cpu_percent = round((total_cpu_used / total_cpu_available) * 100, 2)

        # Staff
        assigned_users = queryset.exclude(assigned_developer__isnull=True).values_list("assigned_developer", flat=True).distinct()
        staff = []
        UserModel = get_user_model()
        for user_id in assigned_users:
            user = UserModel.objects.get(id=user_id)
            staff.append({
                "member": user,
                "processes": queryset.filter(assigned_developer=user)
            })

        context.update({
            "total": total,
            "completed": completed,
            "in_progress": in_progress,
            "average_progress": round(average_progress),
            "processes": queryset,
            "staff": staff,
            "total_memory": total_memory_used,
            "total_cpu": total_cpu_used,
            "memory_percent": memory_percent,
            "cpu_percent": cpu_percent,
        })
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
        project_form = BusinessSystemProjectForm(
            request.POST,
            request.FILES,
            user=request.user    # ← IMPORTANTE
        )

        if project_form.is_valid():
            project = project_form.save(commit=False)
            project.user = request.user  # Asignamos el usuario logueado
            project.save()
            return redirect('business_customer_projects:processes', project_id=project.id)

    else:
        project_form = BusinessSystemProjectForm(user=request.user)  # ← IMPORTANTE

    return render(request, 'create_project.html', {'form': project_form})




from django.shortcuts import get_object_or_404

@login_required
def create_process(request, project_id):

    # Filtrar proyectos SOLO del usuario
    projects = BusinessSystemProject.objects.filter(user=request.user)

    # Asegurar que el proyecto pertenece al usuario
    project = get_object_or_404(BusinessSystemProject, id=project_id, user=request.user)

    if request.method == 'POST':
        process_form = BusinessProcessForm(request.POST)
        if process_form.is_valid():
            process = process_form.save(commit=False)
            process.project = project
            process.save()
            return redirect('automation', project_id=project.id)

    else:
        process_form = BusinessProcessForm()

    return render(
        request,
        'create_process.html',
        {
            'form': process_form,
            'project': project,
            'projects': projects
        }
    )


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





