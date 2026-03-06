from django.urls import path
from .views import social_callback,update_generated_image,update_generated_video,update_carousel_generated_images

app_name = 'core'

urlpatterns = [
    path("social/callback/", social_callback, name="social_callback"),
    path("api/update_image_url/", update_generated_image, name="update_generated_image"),
    path("api/update_video_url/", update_generated_video, name="update_generated_video"),
    path("api/update_carousel_images/", update_carousel_generated_images, name="update_carousel_generated_images"),
]
