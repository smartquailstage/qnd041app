from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from .views import admin_cita_detail
from .sites import custom_admin_site
from usuarios.views import admin_cita_detail

app_name = 'agenda'

urlpatterns = [
    # previous login view 
    path("admin/citas/<int:cita_id>/", views.admin_cita_detail, name="admin_cita_detail"),


]

custom_admin_site.get_urls = lambda: urlpatterns + custom_admin_site.get_urls()

