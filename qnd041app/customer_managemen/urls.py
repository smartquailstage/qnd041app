
from django.urls import path
from .views import WebhookMessageAPIView

app_name = "customer_managemen"

urlpatterns = [
    path('api/webhook-message/', WebhookMessageAPIView.as_view(), name='api-webhook-message'),
]


