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

from django.db.models import Sum, Avg


from django.db.models import Sum, Avg
from django.shortcuts import get_object_or_404

from django.views.generic import DetailView
from django.db.models import Avg, Sum
from .models import BusinessSystemProject, BusinessAutomation

from django.views.generic import DetailView
from django.db.models import Avg, Sum
from .models import BusinessSystemProject, BusinessAutomation, BusinessContracts

from django.views.generic import DetailView
from django.db.models import Avg, Sum
from .models import BusinessSystemProject, BusinessAutomation, BusinessContracts

class BusinessSystemProjectDetailView(DetailView):
    model = BusinessSystemProject
    template_name = "business/project_detail.html"
    context_object_name = "project"

    def safe_percent(self, value):
        """Devuelve un porcentaje seguro entre 0 y 100 con dos decimales."""
        try:
            value = float(value)
        except:
            value = 0
        return round(max(0, min(value, 100)), 2)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.get_object()

        # -------------------
        # PROCESOS
        # -------------------
        processes = project.processes.all()
        total_processes = processes.count()
        completed_processes = processes.filter(progress=100).count()
        in_progress_processes = total_processes - completed_processes
        average_progress = processes.aggregate(avg=Avg("progress"))["avg"] or 0

        total_percent_memory_used = self.safe_percent(
            processes.aggregate(total_mem=Sum("memory_percent_used"))["total_mem"] or 0
        )
        total_percent_cpu_used = self.safe_percent(
            processes.aggregate(total_cpu=Sum("cpu_percent_used"))["total_cpu"] or 0
        )

        context.update({
            "processes": processes,
            "total_processes": total_processes,
            "completed_processes": completed_processes,
            "in_progress_processes": in_progress_processes,
            "average_progress": round(average_progress),
            "total_percent_memory_used": total_percent_memory_used,
            "total_percent_cpu_used": total_percent_cpu_used,
            "processes_completed": processes.filter(progress=100),
            "processes_in_progress": processes.exclude(progress=100),
        })

        # -------------------
        # AUTOMATIZACIÓN
        # -------------------
        automations = project.automations.all()
        total_automations = automations.count()
        completed_automations = automations.filter(progress=100).count()
        total_integrations = automations.filter(automation_category="integration").count()
        average_automation_progress = automations.aggregate(avg=Avg("progress"))["avg"] or 0

        integration_counts = {
            "gov_api": automations.filter(integration_type="gov_api").count(),
            "social_media": automations.filter(integration_type="social_media").count(),
            "electronic_billing": automations.filter(integration_type="electronic_billing").count(),
            "contract_certification": automations.filter(integration_type="contract_certification").count(),
        }

        microservice_counts = {
            key: automations.filter(microservice_type=key).count()
            for key, _ in BusinessAutomation.MICROSERVICE_TYPE_CHOICES
        }

        context.update({
            "automations": automations,
            "total_automations": total_automations,
            "completed_automations": completed_automations,
            "total_integrations": total_integrations,
            "average_automation_progress": round(average_automation_progress),
            "integration_counts": integration_counts,
            "microservice_counts": microservice_counts,
        })

        # -------------------
        # INTELIGENCIA ARTIFICIAL
        # -------------------
        intelligents = project.intelligents.all()
        total_intelligents = intelligents.count()
        completed_intelligents = intelligents.filter(progress=100).count()
        average_intelligent_progress = intelligents.aggregate(avg=Avg("progress"))["avg"] or 0

        context.update({
            "intelligents": intelligents,
            "total_intelligents": total_intelligents,
            "completed_intelligents": completed_intelligents,
            "average_intelligent_progress": round(average_intelligent_progress),
        })

        # -------------------
        # CONTRATOS
        # -------------------
        contracts = project.contracts.all()
        total_contracts = contracts.count()

        contract_type_counts = {
            "ip": contracts.filter(tipo="ip").count(),
            "cloud_services": contracts.filter(tipo="cloud_services").count(),
            "development": contracts.filter(tipo="development").count(),
        }

        context.update({
            "contracts": contracts,
            "total_contracts": total_contracts,
            "contract_type_counts": contract_type_counts,
        })




        # -------------------
        # OTROS DATOS
        # -------------------
        context.update({
            "has_automation": project.has_automation,
            "has_ai": project.has_ai,
            "is_active": project.is_active,
            "staff": project.crew_members.all(),
            "cloud_resources": project.cloud_resources.all(),
        })

        return context



from django.views.generic import ListView
from .models import BusinessAutomation

from django.views.generic import DetailView
from django.db.models import Sum, Avg
from .models import BusinessAutomation

class BusinessAutomationListView(ListView):
    model = BusinessAutomation
    template_name = "business/A.html"
    context_object_name = "automations"
    paginate_by = 20

    def get_queryset(self):
        queryset = BusinessAutomation.objects.all()

        search = self.request.GET.get("search")
        if search:
            queryset = queryset.filter(title__icontains=search)

        automation_type = self.request.GET.get("automation_type")
        if automation_type:
            queryset = queryset.filter(automation_type=automation_type)

        microservice_type = self.request.GET.get("microservice_type")
        if microservice_type:
            queryset = queryset.filter(microservice_type=microservice_type)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        automations = self.get_queryset()

        # 🔹 Estadísticas
        context["total_automations"] = automations.count()
        context["total_integrations"] = automations.filter(automation_category="integration").count()
        context["total_completed"] = automations.filter(progress=100).count()

        # Opciones para filtros
        context["types"] = BusinessAutomation.AUTOMATION_TYPE_CHOICES
        context["microservices"] = BusinessAutomation.MICROSERVICE_TYPE_CHOICES
        context["categories"] = BusinessAutomation.AUTOMATION_CATEGORY_CHOICES

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





from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import PaymentOrder


class PaymentOrderListView(ListView):
    model = PaymentOrder
    template_name = "business/payment_order.html"
    context_object_name = "payment_orders"
    paginate_by = 20
    ordering = "-created_at"

    def get_queryset(self):
        user = self.request.user

        queryset = PaymentOrder.objects.filter(user=user)

        # 🔍 Búsqueda corregida según tu modelo real
        search = self.request.GET.get("search")
        if search:
            queryset = queryset.filter(
                Q(empresa_nombre__icontains=search) |
                Q(ruc__icontains=search) |
                Q(service_type__icontains=search)
            )

        # 🔎 Filtrar por proyecto si se envía ?project=ID
        project_id = self.request.GET.get("project")
        if project_id:
            queryset = queryset.filter(project_id=project_id)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search"] = self.request.GET.get("search", "")
        return context

from django.http import Http404


class PaymentOrderDetailView(DetailView):
    model = PaymentOrder
    template_name = "business/paymentorder_detail.html"
    context_object_name = "payment"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        # 🔒 Seguridad: solo mostrar si es del usuario actual
        if obj.user != self.request.user:
            raise Http404("No tienes permiso para ver esta orden de pago.")

        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        payment = self.get_object()

        context.update({
            "project": payment.project,
            "cost_hour": payment.cost_per_hour,
            "days_until_expiration": payment.days_until_expiration,
            "days_until_final_expiration": payment.days_until_final_expiration,
            "is_expired": payment.is_expired,
            "is_final_expired": payment.is_final_expired,
        })

        return context
