# myapp/custom_admin_urls.py

from django.urls import path
from .views import admin_cita_detail

urlpatterns = [
    path('cita/<int:cita_id>/', admin_cita_detail, name='admin_cita_detail'),
]
