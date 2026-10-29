from django.urls import path
from .views import (
    WebhookMessageAPIView,          # Instagram / Omnicanal Genérico
    WebhookWhatsAppMessageAPIView,  # WhatsApp Cloud API
    WebhookFacebookMessageAPIView,  # Facebook Messenger
)

app_name = "customer_managemen"

urlpatterns = [
    # Endpoint principal (Instagram / Omnicanal)
    path('api/webhook-message/', WebhookMessageAPIView.as_view(), name='api-webhook-message'),
    
    # Endpoints dedicados por plataforma
    path('api/webhook-whatsapp/', WebhookWhatsAppMessageAPIView.as_view(), name='api-webhook-whatsapp'),
    path('api/webhook-facebook/', WebhookFacebookMessageAPIView.as_view(), name='api-webhook-facebook'),
]

