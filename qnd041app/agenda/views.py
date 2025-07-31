from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from usuarios.forms import LoginForm,MensajeForm,CitaForm                   
from usuarios.models import Profile, Cita
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.admin.views.decorators import staff_member_required
import weasyprint
from django.conf import settings
from pathlib import Path
from django.core.cache import cache
from usuarios.models import Dashboard, Mensaje
from django.shortcuts import render
from .models import Cita  # Asegúrate de usar la ruta correcta
from .sites import custom_admin_site



# Create your views here.
@login_required
@staff_member_required
@custom_admin_site.admin_view
def admin_cita_detail(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id)
    context = {
        "title": f"Cita #{cita.id}",
        "breadcrumbs": [
            {"url": "/admin/", "label": "Admin"},
            {"url": "", "label": f"Cita #{cita.id}"},
        ],
        "cards": [
            {
                "title": "Detalle de la cita",
                "icon": "event",
                "items": [
                    {"title": "destinatario", "description": str(cita.destinatario)},
                    {"title": "Fecha", "description": str(cita.fecha)},
                    {"title": "Estado", "description": str(cita.estado or "No definido")}
                ],
            }
        ],
        "cita": cita,
    }
    return render(request, "admin/cita_detail_unfold.html", context)


