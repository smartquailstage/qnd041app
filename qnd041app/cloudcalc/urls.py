from django.urls import path
from . import views

app_name = 'cloudcalc'

urlpatterns = [
    path('', views.estimar_recursos, name='estimar_recursos'),
    path('resultado/<int:estimacion_id>/', views.resultado_estimacion, name='resultado_estimacion'),
]
