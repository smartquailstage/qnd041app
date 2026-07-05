from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path, include
from django.conf.urls.i18n import i18n_patterns
from django.contrib.auth import views as auth_views

from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls
#from wagtail.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import Sitemap
from django.contrib.sitemaps.views import sitemap
from wagtail.models import Page


from django.urls import path
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
# Buscá tus imports de sitemaps y dejalos así:
from wagtail.contrib.sitemaps.views import Sitemap as WagtailSitemap


@csrf_exempt
def robots_txt(request):
    lines = [
        "User-agent: *",
        "Allow: /",
        # Bloqueos de idioma y logins
        "Disallow: /ingresar/",
        "Disallow: */ingresar/",
        "Disallow: /businessmedia/",
        "Disallow: /smartbusinessanalytics/",
        "",
        # Bloqueos de flujos transaccionales (Evita el 'Crawled - currently not indexed')
        "Disallow: */apps_carrito/",
        "Disallow: */apps_metodo_pago/",
        "Disallow: */services_cart/",
        "Disallow: */services_payment/",
        "Disallow: */billing/",
        "Disallow: */platforms_carrito/",
        "Disallow: */platforms_metodo_pago/",
        "Disallow: */iaas_cart/",
        "Disallow: */iaas_payment/",
        "",
        "Sitemap: https://ec.smartquail.io/sitemap.xml"
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")

@csrf_exempt
def sitemap_plano(request):
    # Escupimos el XML crudo como un string puro. Cero base de datos, cero middlewares.
    xml_content = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        '  <url>\n'
        '    <loc>https://ec.smartquail.io/es/</loc>\n'
        '    <changefreq>daily</changefreq>\n'
        '    <priority>1.0</priority>\n'
        '  </url>\n'
        '</urlset>'
    )
    return HttpResponse(xml_content, content_type="application/xml")

# Base (no traducibles)
urlpatterns = [
    path('robots.txt', robots_txt),
   # path('sitemap.xml', sitemap, {'sitemaps': {'wagtail': WagtailSitemap}}, name='django.contrib.sitemaps.views.sitemap'),
    path('sitemap.xml', sitemap_plano, name='sitemap'),
    # ... tus otras rutas
    # ... el resto de tus rutas intac
    
    path('studio_leads_ai/', include('studio_leads_ai.urls', namespace='studio_leads_ai')),

    path('social-auth/', include('social_django.urls', namespace='social')),
    path('tinymce/', include('tinymce.urls')),
    path('rosetta/', include('rosetta.urls')),


    # Wagtail admin y documentos (no traducibles)
    re_path(r'^businessmedia/', include(wagtailadmin_urls), name='wagtail'),
    re_path(r'^documents/', include(wagtaildocs_urls)),
]

# Rutas traducibles (contenido Wagtail y tus apps de frontend)
urlpatterns += i18n_patterns(
    path("smartbusinessanalytics/", admin.site.urls),
   # path('core/', include('core.urls', namespace='core')),
    path('socialmedia_AI/', include('social_media_AI.urls', namespace='social_media_ai')),



    path('estimador/', include('cloudcalc.urls', namespace='cloudcalc')),
    path('smartbusinessanalytics_id/', include('smartbusinessanalytics_id.urls', namespace='smartbusinessanalytics_id')),
    path('smartbusinesslaw/', include('smartbusinesslaw.urls', namespace='smartbusinesslaw')),
    path('smartbusinesslaw_demo/', include('smartbusinesslaw_demo.urls', namespace='smartbusinesslaw_demo')),
    path('activos_itc/', include('business_customer_projects.urls', namespace='business_customer_projects')),
    path('services_cart/', include('services_cart.urls', namespace='services_cart')),
    path('billing/', include('billing.urls', namespace='billing')),
    path('services_payment/', include('services_payment.urls', namespace='services_payment')),
    path('apps_carrito/', include('saas_cart.urls', namespace='saas_cart')),
    path('apps/', include('saas_shop.urls', namespace='saas_shop')),
    path('apps_licencias/', include('saas_orders.urls', namespace='saas_orders')),
    path('apps_convenios/', include('saas_coupons.urls', namespace='saas_coupons')),
    path('apps_metodo_pago/', include('saas_payment.urls', namespace='saas_payment')),




    path('iaas_cart/', include('iaas_cart.urls', namespace='iaas_cart')),
    path('iaas_shop/', include('iaas_shop.urls', namespace='iaas_shop')),
    path('iaas_orders/', include('iaas_orders.urls', namespace='iaas_orders')),
    path('iaas_coupons/', include('iaas_coupons.urls', namespace='iaas_coupons')),
    path('iaas_payment/', include('iaas_payment.urls', namespace='iaas_payment')),


    path('platforms_carrito/', include('paas_cart.urls', namespace='paas_cart')),
    path('platforms/', include('paas_shop.urls', namespace='paas_shop')),
    path('platforms_licencias/', include('paas_orders.urls', namespace='paas_orders')),
    path('platforms_convenios/', include('paas_coupons.urls', namespace='paas_coupons')),
    path('platforms_metodo_pago/', include('paas_payment.urls', namespace='paas_payment')),
    path('contrato/', include('smartcontracts.urls', namespace='smartcontracts')),

   # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
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
    path('ingresar/', include('usuarios.urls', namespace='usuarios')),
    path('sbmshop/', include('sbmshop.urls', namespace='sbmshop')),
    path('sbashop/', include('sbashop.urls', namespace='sbashop')),
    path('sblshop/', include('sblshop.urls', namespace='sblshop')),
    path('sbtshop/', include('sbtshop.urls', namespace='sbtshop')),
    path('sbpshop/', include('sbpshop.urls', namespace='sbpshop')),

    # Wagtail frontend (las páginas creadas en el CMS)
    path("", include(wagtail_urls)),
    prefix_default_language=True
)

# Archivos estáticos y media en desarrollo
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
