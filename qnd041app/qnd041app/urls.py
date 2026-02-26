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


    # Wagtail admin y documentos (no traducibles)
    re_path(r'^businessmedia/', include(wagtailadmin_urls), name='wagtail'),
    re_path(r'^documents/', include(wagtaildocs_urls)),
]

# Rutas traducibles (contenido Wagtail y tus apps de frontend)
urlpatterns += i18n_patterns(
    path('core/', include('core.urls', namespace='core')),
    path('estimador/', include('cloudcalc.urls', namespace='cloudcalc')),
    path('smartbusinessanalytics_id/', include('smartbusinessanalytics_id.urls', namespace='smartbusinessanalytics_id')),
    path('smartbusinesslaw/', include('smartbusinesslaw.urls', namespace='smartbusinesslaw')),
    path('business_customer_projects/', include('business_customer_projects.urls', namespace='business_customer_projects')),
    path('services_cart/', include('services_cart.urls', namespace='services_cart')),
    path('billing/', include('billing.urls', namespace='billing')),
    path('services_payment/', include('services_payment.urls', namespace='services_payment')),
    path('saas_cart/', include('saas_cart.urls', namespace='saas_cart')),
    path('saas_shop/', include('saas_shop.urls', namespace='saas_shop')),
    path('saas_orders/', include('saas_orders.urls', namespace='saas_orders')),
    path('saas_coupons/', include('saas_coupons.urls', namespace='saas_coupons')),
    path('saas_payment/', include('saas_payment.urls', namespace='saas_payment')),


    path('paas_cart/', include('paas_cart.urls', namespace='paas_cart')),
    path('paas_shop/', include('paas_shop.urls', namespace='paas_shop')),
    path('paas_orders/', include('paas_orders.urls', namespace='paas_orders')),
    path('paas_coupons/', include('paas_coupons.urls', namespace='paas_coupons')),
    path('paas_payment/', include('paas_payment.urls', namespace='paas_payment')),
    path('contrato/', include('smartcontracts.urls', namespace='smartcontracts')),

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('i18n/', include('django.conf.urls.i18n')),  # Selector de idioma



    #path('cart/', include('cart.urls', namespace='cart')),
    #path('shop/', include('shop.urls', namespace='shop')),
    #path('orders/', include('orders.urls', namespace='orders')),
    #path('coupons/', include('coupons.urls', namespace='coupons')),
    #path('payment/', include('payment.urls', namespace='payment')),
   # path('sqorders/', include('SQOrders.urls', namespace='sqorders')),
    path('itc_business/', include('usuarios.urls', namespace='usuarios')),
    path('sbmshop/', include('sbmshop.urls', namespace='sbmshop')),
    path('sbashop/', include('sbashop.urls', namespace='sbashop')),
    path('sblshop/', include('sblshop.urls', namespace='sblshop')),
    path('sbtshop/', include('sbtshop.urls', namespace='sbtshop')),
    path('sbpshop/', include('sbpshop.urls', namespace='sbpshop')),

    # Wagtail frontend (las páginas creadas en el CMS)
    path("", include(wagtail_urls)),
)

# Archivos estáticos y media en desarrollo
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
