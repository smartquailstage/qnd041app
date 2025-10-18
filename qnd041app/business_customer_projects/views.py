from django.views.generic.detail import DetailView
from .models import BusinessSystemProject

class BusinessSystemProjectDetailView(DetailView):
    model = BusinessSystemProject
    template_name = "business/project_detail.html"
    context_object_name = "project"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.get_object()

        # Obtener los procesos relacionados
        processes = project.processes.all()
        context["processes"] = processes

        # Obtener recursos cloud
        context["cloud_resources"] = project.cloud_resources.all()

        # Agregar lógica para pestañas condicionales
        context["has_automation"] = processes.filter(has_automation=True).exists()
        context["has_ai"] = processes.filter(has_ai=True).exists()

        # (Opcional) si necesitas personal a cargo, agregar aquí:
        context["staff"] = project.assigned_personnel.all() if hasattr(project, 'assigned_personnel') else []

        return context
