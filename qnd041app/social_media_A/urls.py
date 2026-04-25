from django.urls import path
from .views import n8n_webhook_callback

urlpatterns = [
    path("webhooks/n8n/", n8n_webhook_callback, name="n8n-webhook"),
]