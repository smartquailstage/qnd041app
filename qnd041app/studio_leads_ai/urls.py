from django.urls import path
from .views import (
    whatsapp_webhook,
    whatsapp_verify
)


app_name = "studio_leads_ai"


urlpatterns = [
    path(
        "webhook/whatsapp/",
        whatsapp_webhook
    ),

    path(
        "webhook/whatsapp/verify/",
        whatsapp_verify
    ),
]