from django.urls import path
from .views import enviar_mailing_view, previsualizar_mailing_view

app_name = 'mailing'

urlpatterns = [
    path('enviar/<int:pk>/', enviar_mailing_view, name='enviar_mailing_admin'),
    path('previsualizar/<int:pk>/', previsualizar_mailing_view, name='previsualizar_mailing'),
]