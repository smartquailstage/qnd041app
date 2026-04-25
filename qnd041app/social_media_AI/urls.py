from django.urls import path
from .views import n8n_webhook_callback

from django.urls import path
from .views import n8n_instagram_webhook, save_generated_image_to_wagtail


app_name = 'social_media_AI'


urlpatterns = [
    path("webhooks/wagtail/save-image/", save_generated_image_to_wagtail),
    path("webhooks/n8n/instagram/post", n8n_instagram_webhook,name="n8n-instagram-post-webhook"),
    path("webhooks/n8n/", n8n_webhook_callback, name="n8n-webhook"),
]