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

import matplotlib.pyplot as plt
#import seaborn as sns
import numpy as np
import io
import base64
from datetime import date
from django.utils import timezone

from .models import MonthlySystemMetrics  # Asegúrate de tener este modelo


from django.views.generic import DetailView
from django.db.models import Avg, Sum
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
from .models import BusinessSystemProject, BusinessAutomation, MonthlySystemMetrics
class BusinessSystemProjectDetailView(DetailView):
    model = BusinessSystemProject
    template_name = "business/project_detail.html"
    context_object_name = "project"

    def safe_percent(self, value):
        try:
            value = float(value)
        except Exception:
            value = 0
        return round(max(0, min(value, 100)), 2)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.get_object()

        # -------------------
        # PROCESOS
        # -------------------
        processes = project.processes.all()
        context.update({
            "processes": processes,
            "total_processes": processes.count(),
            "completed_processes": processes.filter(progress=100).count(),
            "in_progress_processes": processes.exclude(progress=100).count(),
            "average_progress": round(processes.aggregate(avg=Avg("progress"))["avg"] or 0),
            "total_percent_memory_used": self.safe_percent(
                processes.aggregate(total=Sum("memory_percent_used"))["total"] or 0
            ),
            "total_percent_cpu_used": self.safe_percent(
                processes.aggregate(total=Sum("cpu_percent_used"))["total"] or 0
            ),

            "total_percent_store_used": self.safe_percent(
                processes.aggregate(total=Sum("storage_percent_used"))["total"] or 0
            ),

        })

        # -------------------
        # AUTOMATIZACIÓN
        # -------------------
        automations = project.automations.all()
        context.update({
            "automations": automations,
            "total_automations": automations.count(),
            "completed_automations": automations.filter(progress=100).count(),
            "average_automation_progress": round(
                automations.aggregate(avg=Avg("progress"))["avg"] or 0
            ),
        })

        # -------------------
        # IA
        # -------------------
        intelligents = project.intelligents.all()
        context.update({
            "intelligents": intelligents,
            "total_intelligents": intelligents.count(),
            "completed_intelligents": intelligents.filter(progress=100).count(),
            "average_intelligent_progress": round(
                intelligents.aggregate(avg=Avg("progress"))["avg"] or 0
            ),
        })

        # -------------------
        # CONTRATOS
        # -------------------
        contracts = project.contracts.all()
        context.update({
            "contracts": contracts,
            "total_contracts": contracts.count(),
        })

        # -------------------
        # MÉTRICAS + HORAS
        # -------------------
        metrics = MonthlySystemMetrics.objects.filter(project=project).order_by("date")

        total_hours_used = round(
            sum(m.total_hours for m in metrics), 2
        )

        hours = int(total_hours_used)
        minutes = int(round((total_hours_used - hours) * 60))

        context["total_hours_used"] = total_hours_used
        context["total_hours_used_h"] = hours
        context["total_hours_used_min"] = minutes

        # -------------------
        # GRÁFICO DE RECURSOS (3 HISTOGRAMAS SUPERPUESTOS)
        # -------------------
        if metrics.exists():
            dates = [m.date.strftime("%b %Y") for m in metrics]
            x = np.arange(len(dates))
            width = 0.6

            almacenamiento = np.array([m.almacenamiento_gb or 0 for m in metrics])
            procesamiento = np.array([m.procesamiento_millicore or 0 for m in metrics])
            memoria = np.array([m.memoria_gb or 0 for m in metrics])

            max_almacenamiento = project.almacenamiento_aproximado_gb or 0
            max_procesamiento = project.procesamiento_total_aproximado_millicore or 0
            max_memoria = project.memoria_aproximada_gb or 0

            fig, axs = plt.subplots(3, 1, figsize=(10, 12), sharex=True)
            fig.patch.set_facecolor("#2e2e2e")

            for ax in axs:
                ax.set_facecolor("#2e2e2e")
                ax.tick_params(colors="#ffab4d")
                for spine in ax.spines.values():
                    spine.set_color("#ffab4d")
                ax.yaxis.label.set_color("#ffab4d")
                ax.title.set_color("#ffab4d")
                ax.grid(color="#555555", linestyle="--", linewidth=0.5)

            # Almacenamiento
            axs[0].bar(x, [max_almacenamiento] * len(x),
                       width=width, color="tab:blue", alpha=0.25)
            axs[0].bar(x, almacenamiento,
                       width=width, color="tab:blue", alpha=0.9)
            axs[0].set_ylabel("Almacenamiento (GB)")
           

            # Procesamiento
            axs[1].bar(x, [max_procesamiento] * len(x),
                       width=width, color="tab:orange", alpha=0.25)
            axs[1].bar(x, procesamiento,
                       width=width, color="tab:orange", alpha=0.9)
            axs[1].set_ylabel("Procesamiento (millicore)")
            

            # Memoria
            axs[2].bar(x, [max_memoria] * len(x),
                       width=width, color="tab:green", alpha=0.25)
            axs[2].bar(x, memoria,
                       width=width, color="tab:green", alpha=0.9)
            axs[2].set_ylabel("Memoria RAM (GB)")
           

            axs[2].set_xticks(x)
            axs[2].set_xticklabels(dates, rotation=45, color="#ffab4d")

            plt.tight_layout()

            buffer = io.BytesIO()
            plt.savefig(buffer, format="png", facecolor=fig.get_facecolor())
            plt.close()
            buffer.seek(0)

            context["resource_graph"] = base64.b64encode(
                buffer.getvalue()
            ).decode("utf-8")
            context["monthly_metrics"] = metrics

            buffer.close()
        else:
            context["resource_graph"] = None
            context["monthly_metrics"] = []

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
    paginate_by = 5
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


from django.http import Http404
from django.views.generic import DetailView
from services_cart.cart import Cart
#from shop.recommender import Recommender
from business_customer_projects.models import PaymentOrder


from django.http import Http404
from django.views.generic import DetailView



class PaymentOrderDetailView(DetailView):
    model = PaymentOrder
    template_name = "business/paymentorder_detail.html"
    context_object_name = "payment"  # ya disponible en template como {{ payment }}

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        # Seguridad: solo el usuario asignado puede ver la orden
        if obj.user != self.request.user:
            raise Http404("No tienes permiso para ver esta orden de pago.")

        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Instancia del carrito
        cart = Cart(self.request)

        # Actualizamos el contexto
        context.update({
            "project": self.object.project,
            "cost_with_iva": self.object.cost_with_iva,
            "cost_hour": self.object.hourly_cost,
            "cart": cart,
            "payment": self.object,   # Aseguramos que template pueda usar {{ payment.id }}
            "in_cart": str(self.object.id) in cart.cart,  # Para deshabilitar botón si ya está en carrito
        })

        return context







from django.views.generic import ListView
from .models import Noticia, CategoriaNoticia


class NoticiaListView(ListView):
    model = Noticia
    template_name = 'noticias/noticia_list.html'
    context_object_name = 'noticias'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['noticias_itc'] = Noticia.objects.filter(
            activa=True, categoria__slug='itc'
        )

        context['noticias_id'] = Noticia.objects.filter(
            activa=True, categoria__slug='i_d'
        )

        context['noticias_automatizacion'] = Noticia.objects.filter(
            activa=True, categoria__slug='automatizacion'
        )

        context['noticias_ia'] = Noticia.objects.filter(
            activa=True, categoria__slug='ia'
        )

        context['noticias_seguridad'] = Noticia.objects.filter(
            activa=True, categoria__slug='seguridad'
        )

        context['noticias_monitoring'] = Noticia.objects.filter(
            activa=True, categoria__slug='monitoring'
        )

        context['noticias_recursos'] = Noticia.objects.filter(
            activa=True, categoria__slug='recursos'
        )

        return context






from .models import Noticia
from .forms import ComentarioNoticiaForm


class NoticiaDetailView(DetailView):
    model = Noticia
    template_name = 'noticias/noticia_detalle.html'
    context_object_name = 'noticia'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_comentario'] = ComentarioNoticiaForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = ComentarioNoticiaForm(request.POST)

        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.noticia = self.object
            comentario.usuario = request.user
            comentario.save()
            return redirect(request.path)

        context = self.get_context_data()
        context['form_comentario'] = form
        return self.render_to_response(context)



# views.py
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
import json
from .models import Noticia, NoticiaMetricas

@login_required
@require_POST
def actualizar_metricas(request, pk):
    data = json.loads(request.body)
    action = data.get('action')

    try:
        noticia = Noticia.objects.get(pk=pk)
        metricas, created = NoticiaMetricas.objects.get_or_create(noticia=noticia)

        if action == 'like':
            metricas.likes += 1
        elif action == 'share_social':
            metricas.compartidos_redes += 1
        elif action == 'share_email':
            metricas.compartidos_email += 1
        elif action == 'download':
            metricas.descargas += 1

        metricas.save()

        return JsonResponse({
            'success': True,
            'likes': metricas.likes,
            'compartidos_redes': metricas.compartidos_redes,
            'compartidos_email': metricas.compartidos_email,
            'descargas': metricas.descargas
        })

    except Noticia.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Noticia no encontrada'})




from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.shortcuts import redirect
from .models import SupportTicket
from .forms import SupportTicketForm


class SupportTicketListView(LoginRequiredMixin, ListView):
    model = SupportTicket
    template_name = 'tickets/ticket_list.html'
    context_object_name = 'tickets'
    paginate_by = 10

    def get_queryset(self):
        queryset = SupportTicket.objects.filter(user=self.request.user)

        status = self.request.GET.get('status')
        if status in ['active', 'finished']:
            queryset = queryset.filter(status=status)

        return queryset.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SupportTicketForm()
        return context

    def post(self, request, *args, **kwargs):
        """
        Maneja la creación del ticket desde el ListView
        """
        form = SupportTicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.status = 'active'
            ticket.save()
            return redirect('ticket_list')

        self.object_list = self.get_queryset()
        return self.render_to_response(
            self.get_context_data(form=form)
        )


from django.utils import timezone
from django.http import HttpResponseForbidden


class SupportTicketDetailView(LoginRequiredMixin, DetailView):
    model = SupportTicket
    template_name = 'tickets/ticket_detail.html'
    context_object_name = 'ticket'

    def get_queryset(self):
        return SupportTicket.objects.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        """
        Permite cerrar el ticket desde el detalle
        """
        ticket = self.get_object()

        if ticket.status == 'active':
            ticket.status = 'finished'
            ticket.finished_at = timezone.now()
            ticket.save()
            return redirect('ticket_detail', pk=ticket.pk)

        return HttpResponseForbidden()
