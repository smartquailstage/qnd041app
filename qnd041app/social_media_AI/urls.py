from django.urls import path
from .views import n8n_webhook_callback

from django.urls import path
from .views import SaveGeneratedImageView,InstagramWebhookView,GenericWebhookCallbackView,


app_name = 'social_media_AI'


urlpatterns = [
    path("webhook/save-image/", SaveGeneratedImageView.as_view()),
    path("webhook/instagram/", InstagramWebhookView.as_view()),
    path("webhook/callback/", GenericWebhookCallbackView.as_view()),
]