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




