from django.urls import path

from .views import (
    save_generated_image,
    instagram_webhook,
    generic_callback
)

app_name = "social_media_AI"

urlpatterns = [
    path(
        "webhooks/wagtail/save-image/",
        update_generated_image,
        name="update_generated_image"
    ),

    path(
        "webhooks/n8n/instagram/post",
        instagram_webhook,
        name="n8n-instagram-post-webhook"
    ),

    path(
        "webhooks/n8n/",
        generic_callback,
        name="n8n-webhook"
    ),
]