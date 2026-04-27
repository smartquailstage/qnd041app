from django.urls import path
from .views import SaveGeneratedImageView,InstagramWebhookView,GenericWebhookCallbackView


app_name = 'social_media_AI'


urlpatterns = [
    path("webhooks/wagtail/save-image/", SaveGeneratedImageView),
    path("webhooks/n8n/instagram/post", InstagramWebhookView, name="n8n-instagram-post-webhook"),
    path("webhooks/n8n/", GenericWebhookCallbackView, name="n8n-webhook"),
]