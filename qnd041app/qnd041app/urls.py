from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path, include
from django.conf.urls.i18n import i18n_patterns
from django.contrib.auth import views as auth_views

from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls

# Base (no traducibles)
urlpatterns = [
    path("smartbusinessanalytics/", admin.site.urls),
   # path("admin/", dashboard_view),
  #  path('admin/citas/', include((custom_admin_urls.urlpatterns, 'custom_admin'))),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('tinymce/', include('tinymce.urls')),
    path('rosetta/', include('rosetta.urls')),

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('i18n/', include('django.conf.urls.i18n')),  # Selector de idioma

    # Wagtail admin y documentos (no traducibles)
    re_path(r'^businessmedia/', include(wagtailadmin_urls), name='wagtail'),
    re_path(r'^documents/', include(wagtaildocs_urls)),
]

# Rutas traducibles (contenido Wagtail y tus apps de frontend)
urlpatterns += i18n_patterns(
    path('webapp/', include('usuarios.urls', namespace='usuarios')),
    path('sbmshop/', include('sbmshop.urls', namespace='sbmshop')),
    path('sbashop/', include('sbashop.urls', namespace='sbashop')),
    path('sblshop/', include('sblshop.urls', namespace='sblshop')),
    path('sbtshop/', include('sbtshop.urls', namespace='sbtshop')),

    # Wagtail frontend (las páginas creadas en el CMS)
    path("", include(wagtail_urls)),
)

# Archivos estáticos y media en desarrollo
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
