from django.urls import path
from .views import social_callback

urlpatterns = [
    path("social/callback/", social_callback, name="social_callback"),
]