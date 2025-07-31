"""
URL configuration for qnd41app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, re_path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views as auth_views
from usuarios.views import dashboard_view
from usuarios.views import admin_cita_detail
import usuarios.custom_admin_urls as custom_admin_urls

from django.conf.urls.i18n import i18n_patterns
from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail import urls as wagtaildocs_urls



#from agenda.sites import custom_admin_site


# Change the parentheses to square brackets for a list
urlpatterns = [
    path("smartbusinessanalytics/", admin.site.urls),
    path('tinymce/', include('tinymce.urls')),
   # path("admin2/", custom_admin_site.urls),
   # path("Agenda_Meddes/", include("agenda.urls")),
  #  path("Citas_regulares/", include("citas_regulares.urls")),
    path("admin/", dashboard_view),
  
    #path("admin/citas/<int:cita_id>/", admin_cita_detail, name="admin_cita_detail"),
    path('admin/citas/', include((custom_admin_urls.urlpatterns,'custom_admin'))),
    #path('calendario/', include('schedule.urls')),
  #  path('calendar/', include('calendarium.urls'))
    #path('inicio/', admin.site.urls),
 #   path('appointment/', include('appointment.urls')),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('rosetta/', include('rosetta.urls')),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('webapp/', include('usuarios.urls', namespace='usuarios')),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('i18n/', include('django.conf.urls.i18n')),
    path('sbmshop/', include('sbmshop.urls', namespace='sbmshop')),
    path('sbashop/', include('sbashop.urls', namespace='sbashop')),
    path('sblshop/', include('sblshop.urls', namespace='sblshop')),
    path('sbtshop/', include('sbtshop.urls', namespace='sbtshop')),
    
    #path('calendario/', self.admin_site.admin_view(self.calendar_view), name='citas_calendar'),
    # reset password urls
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    re_path(r'^businessmedia/', include(wagtailadmin_urls),name='wagtail'),
    re_path(r'^documents/', include(wagtaildocs_urls)),
    re_path(r'', include(wagtail_urls)),
   

]

# Add static URLs to the urlpatterns if in debug mode
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
