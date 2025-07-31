# agenda/urls_admin.py
from django.urls import path
from .admin_views import admin_cita_detail

urlpatterns = [
    path("cita/<int:cita_id>/detalle/", admin_cita_detail, name="admin_cita_detail"),
]
