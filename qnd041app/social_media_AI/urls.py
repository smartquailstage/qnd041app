from django.urls import path

from .views import (
    SaveGeneratedImageView,
    InstagramWebhookView,
    GenericWebhookCallbackView
)

app_name = "social_media_AI"

urlpatterns = [
    path(
        "webhooks/wagtail/save-image/",
        SaveGeneratedImageView.as_view(),
        name="save-image"
    ),

    path(
        "webhooks/n8n/instagram/post",
        InstagramWebhookView.as_view(),
        name="n8n-instagram-post-webhook"
    ),

    path(
        "webhooks/n8n/",
        GenericWebhookCallbackView.as_view(),
        name="n8n-webhook"
    ),
]