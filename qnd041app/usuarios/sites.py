# admin_site.py
from unfold.sites import UnfoldAdminSite
from django.urls import path
from django.template.response import TemplateResponse
from usuarios.models import Cita  # importa tu modelo

class CustomAdminSite(UnfoldAdminSite):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("", self.admin_view(self.custom_dashboard), name="index"),
        ]
        return custom_urls + urls

    def custom_dashboard(self, request):
        citas = Cita.objects.all()
        events = [
            {
                "title": c.motivo,
                "start": c.fecha.isoformat(),
                #"end": c.fecha_fin.isoformat(),
            }
            for c in citas
        ]
        return TemplateResponse(request, "admin/dashboard_calendar.html", {"events": events})

custom_admin_site = CustomAdminSite(name="custom_admin_site")
