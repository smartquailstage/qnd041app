from django.urls import path
from .views import social_callback,update_generated_image

urlpatterns = [
    path("social/callback/", social_callback, name="social_callback"),
    path("api/update_image_url/", update_generated_image, name="update_generated_image"),
]

