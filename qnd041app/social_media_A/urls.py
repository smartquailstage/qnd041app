from django.urls import path
from .views import n8n_webhook_callback
from .views import n8n_instagram_webhook

urlpatterns = [
    path("webhooks/n8n/", n8n_webhook_callback, name="n8n-webhook"),
    path('api/webhooks/social_media_A_instagram/', n8n_instagram_webhook, name='n8n_instagram_webhook'),
]