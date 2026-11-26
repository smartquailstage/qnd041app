from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.urls import NoReverseMatch, reverse


def _safe_reverse(view_name):
    try:
        return reverse(view_name)
    except NoReverseMatch:
        return "#"


@staff_member_required
def building_admin_dashboard(request):
    context = {
        **admin.site.each_context(request),
        "title": "Dashboard Gestión de Edificios",
        "modulo": "SmartBuildingAdmin",
        "urls": {
            "admin_index": _safe_reverse("admin:index"),
            "edificios": _safe_reverse("admin:building_admin_edificio_changelist"),
            "areas_comunes": _safe_reverse("admin:building_admin_areacomun_changelist"),
            "limpieza": _safe_reverse("admin:building_admin_registrolimpieza_changelist"),
            "mantenimiento": _safe_reverse("admin:building_admin_ordenmantenimiento_changelist"),
            "unidades": _safe_reverse("admin:building_admin_unidad_changelist"),
            "alicuotas": _safe_reverse("admin:building_admin_cargoalicuota_changelist"),
            "documentos": _safe_reverse("admin:building_admin_documentonormativo_changelist"),
            "fragmentos": _safe_reverse("admin:building_admin_fragmentonormativo_changelist"),
            "agente_ia": _safe_reverse("admin:ai_agent_agentsoul_changelist"),
        },
    }
    return render(request, "admin/smartbuildingadmin/dashboard.html", context)