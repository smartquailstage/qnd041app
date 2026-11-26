from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

app_name = 'building_admin'

urlpatterns = [


    path("dashboard/", views.building_admin_dashboard, name="building_admin_dashboard"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    










