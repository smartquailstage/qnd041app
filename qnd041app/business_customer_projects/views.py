from django.views.generic.detail import DetailView
from .models import BusinessSystemProject

class BusinessSystemProjectDetailView(DetailView):
    model = BusinessSystemProject
    template_name = "business/project_detail.html"
    context_object_name = "project"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.get_object()

        # Obtener procesos
        processes = project.processes.all()
        context["processes"] = processes

        # Recursos cloud
        context["cloud_resources"] = project.cloud_resources.all()

        # Pestañas condicionales
        context["has_automation"] = processes.filter(has_automation=True).exists()
        context["has_ai"] = processes.filter(has_ai=True).exists()

        # ✅ Personal a cargo (SmartQuailCrew)
        context["staff"] = project.crew_members.all()  # Usa el nombre real del campo

        return context

