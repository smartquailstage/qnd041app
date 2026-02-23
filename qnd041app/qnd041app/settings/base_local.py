

import os
from pathlib import Path
from dotenv import load_dotenv
from django.utils.translation import gettext_lazy as _
from django.templatetags.static import static
from django.urls import reverse_lazy
from decouple import config, Csv







BASE_DIR = Path(__file__).resolve().parent.parent
# Load environment variables from the .env_local file.
ENV_FILE_PATH = BASE_DIR / ".env_local"
load_dotenv(dotenv_path=ENV_FILE_PATH)

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = config("EMAIL_HOST", default="127.0.0.1")
EMAIL_PORT = config("EMAIL_PORT", cast=int, default=25)
EMAIL_USE_TLS = config("EMAIL_USE_TLS", cast=bool, default=False)
EMAIL_USE_SSL = config("EMAIL_USE_SSL", cast=bool, default=False)

EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")

DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", default="support@smartquail.io")
SERVER_EMAIL = config("SERVER_EMAIL", default="support@smartquail.io")



ADMINS = [
    ("Soporte Meddes", "info@meddes.com.ec"),
    # ("Otro Nombre", "otro@correo.com"),  # Puedes agregar más si deseas
]

# Retrieve the Django secret key from environment variables.
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

ALLOWED_HOSTS = ['tusitio.com', '127.0.0.1'] 

# Configura DEBUG usando variable de entorno o por defecto False
DEBUG = config('DEBUG', default=False, cast=bool)

if DEBUG:
    ADMINS = []
else:
    # En producción, define tus administradores correctamente:
    ADMINS = [
        ("Soporte SmartQuail", "support@smartquail.io"),
    ]

    


# Variable que define si estás en entorno local
ENVIRONMENT = config("ENVIRONMENT", default="local")  # local, staging, production

if ENVIRONMENT == "local":
    EMAIL_BACKEND = config("EMAIL_BACKEND")
    EMAIL_HOST = config("EMAIL_HOST")
    EMAIL_PORT = config("EMAIL_PORT", cast=int)
    EMAIL_USE_TLS = config("EMAIL_USE_TLS", cast=bool)
    EMAIL_USE_SSL = config("EMAIL_USE_SSL", cast=bool)
    EMAIL_HOST_USER = config("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
    DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
else:
    # Configuración de producción u otros entornos
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = "smtp.gmail.com"
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_USE_SSL = False
    EMAIL_HOST_USER = "phys.mauiricio.silva@gmail.com"
    EMAIL_HOST_PASSWORD = "secreto_produccion"
    DEFAULT_FROM_EMAIL = EMAIL_HOST_USER



# Optionally, you can add a default value or raise an exception if SECRET_KEY is not set
if SECRET_KEY is None:
    raise ValueError("DJANGO_SECRET_KEY is not set in the environment variables.")
# Obtener variable de entorno (lanzar error si no existe)




SITE_DOMAIN = os.environ.get('SITE_DOMAIN', 'http://localhost:8000')  # Cambia esto según tu configuración



INSTALLED_APPS = [
    # Unfold (debe ir antes del admin)
 
    "unfold",
    "unfold.contrib.forms",
    "unfold.contrib.filters",  # opcional
    "unfold.contrib.inlines",  # opcional
    "unfold.contrib.import_export",  # opcional
    "unfold.contrib.guardian",  # opcional
    "unfold.contrib.simple_history",

    # Django core apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    'django.contrib.sites', 
 
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    'multiselectfield',
    #'citas_regulares',

    "core",
    "webapp",

    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    
     
    'wagtail',
   # 'cart',
   # 'orders',
   # 'shop',
    

  #  "wagtail.search",
  #  "wagtail.sites",
  #  "wagtail.locales",
    "wagtail_localize", 
    "wagtail_localize.locales",
    "wagtailmedia",
#    "wagtail.contrib.forms",
 #   "wagtail.contrib.redirects",
    "wagtail.contrib.routable_page",
    "wagtail.contrib.settings",

    # Wagtail plugins
    "wagtailgmaps",
    "wagtailmenus",
    # "wagtail_modeltranslation",  # Descomentar si se usa
 

    # Terceros / externos
    "rest_framework",
    "ckeditor",
    'smartcontracts',
    "djmoney",
    "localflavor",
    "boto3",
    "storages",
    "sorl.thumbnail",
    "embed_video",
    "social_django",
    "django_celery_beat",
    "django_celery_results",
    "django_extensions",
    "widget_tweaks",
    "django_forms_bootstrap",
    "bootstrap4",
    "bootstrap5",
    "bootstrap_datepicker_plus",
    "jquery",
    "qr_code",
    "tinymce",
    "phone_field",
    "phonenumber_field",
    "django_social_share",
    "business_customer_projects",
    'smartbusinessanalytics_id',

             # Apps propias del proyecto
    "usuarios",
    #'businees_customers_projects',
    #"SQOrders",
    #"SQShop",
    'chatbot_ai',
   
   
    "serviceapp",
    'billing',
    #"citas_regulares",

    # E-commerce apps
    "cloudcalc",
    #"coupons",
    #PAAS
    'paas_shop',
    'paas_cart',
    'paas_orders',
    'paas_coupons',
    'paas_payment',
    #SAAS
    'saas_shop',
    'saas_orders',
    'saas_cart',
    'saas_coupons',
    'saas_payment',

    #SmartBusinessANALYTICS
    "sbacart",
    "sbashop",
    "sbaorders",
    #SmartBusinessLaw
    "sblcart",
    "sblshop",
    "sblorders",
    'sbpshop',

    #SmartBusinessTechonologies 
    "sbtcart",
    "sbtshop",
    "sbtorders",
    #SmartBusinessMedia
    "sbmcart",
    "sbmshop",
    "sbmorders",
    "sbmcoupons",
    'smartbusinesslaw',
    "sbmpayments",
    #"sbacart",
    #"sbashop",
    #"sbaorders",
    "services_cart",
    "services_coupons",
    "services_payment",
    "rosetta",
    "taggit"
]

#LOGINGS REDIRECT

LOGIN_REDIRECT_URL = 'usuarios:perfil'
LOGIN_URL = 'usuarios:login'
LOGOUT_URL = 'usuarios:logout'

SITE_ID = 1


domain = os.environ.get('SITE_DOMAIN', 'http://localhost:8000')

CART_SESSION_ID = 'cart'

SAAS_CART_SESSION_ID = 'saas_cart'
PAAS_CART_SESSION_ID = 'paas_cart'

SERVICES_CART_SESSION_ID = 'services_cart'

from usuarios.utils import  permission_callback,permission_callback_prospecion




def badge_color_callback(request):
    count = 1  # Cambia este valor para probar diferentes colores

    if count == 0:
        return "info"
    elif count < 2:
        return "info"  # si tienes una clase para warning
    else:
        return "info"



def is_terapeuta(request):
    return request.user.groups.filter(name="terapeutico").exists()

def is_administrativo(request):
    return request.user.groups.filter(name="administrativo").exists()

def is_financiero(request):
    return request.user.groups.filter(name="financiero").exists()

def is_institucional(request):
    return request.user.groups.filter(name="institucional").exists()

def is_superuser(request):
    return request.user.is_superuser

def is_administrativo_o_isuperuser(request):
    return is_administrativo(request) or is_superuser(request)

def is_institucional_o_terapeuta_o_administrativo(request):
    return is_institucional(request) or is_terapeuta(request)  or is_administrativo(request)  or is_superuser(request)

def is_institucional_o_administrativo(request):
    return is_institucional(request)   or is_administrativo(request) or is_superuser(request)

def is_admin_o_terapeuta(request):
    return is_administrativo(request) or is_terapeuta(request) or is_superuser(request)

def is_admin_o_financiero(request):
    return is_administrativo(request) or is_financiero(request) or is_superuser(request)

def is_all(request):
    return is_administrativo(request) or is_financiero(request) or is_superuser(request) or is_terapeuta(request) or is_institucional(request)




UNFOLD = {
    "SITE_TITLE": "SmartQuail IT Cloud Business (I+D)®      Planificador de Recursos Empresariales",
    "SITE_HEADER": "SmartQuail",
    "SHOW_LANGUAGES": False,
    "SITE_SUBHEADER": "Eterprises Research & Development",
    "SITE_DESCRIPTION": "SmartQuail.S.A.S (I+D)",
    "SITE_COPYRIGHT": "Copyright © 2025 SmartQuail S.A.S Todos los derechos reservados.",
    "DASHBOARD_CALLBACK": "usuarios.views.dashboard_callback",
    "SITE_DROPDOWN": [
        {"icon": "person", "title": _("Usuarios(AUTH)"), "link": reverse_lazy("admin:auth_user_changelist")},
        {"icon": "key", "title": _("Roles(RBAC)"), "link": reverse_lazy("admin:auth_group_changelist")},
        {"icon": "people", "title": _("Institucionales"), "link": reverse_lazy("admin:usuarios_perfilinstitucional_changelist")},
         {"icon": "people", "title": _("Terapeutas"), "link": reverse_lazy("admin:usuarios_perfil_terapeuta_changelist")},
        
        
        {"icon": "map", "title": _("Regulaciones"), "link": reverse_lazy("admin:smartbusinesslaw_regulacion_changelist")},
        {"icon": "circle", "title": _("Monitoreo"), "link": reverse_lazy("admin:django_celery_results_taskresult_changelist")},
         {"icon": "support", "title": _("Soporte"), "link": reverse_lazy("admin:usuarios_cliente_changelist")},
    ],
    "SITE_URL": "https://ec.smartquail.io",
    "SITE_ICON": {"light": lambda request: static("img/BA-LOGOS/loro.png"), "dark": lambda request: static("img/BA-LOGOS/loro.png")},
    "SITE_LOGO": {"light": lambda request: static("img/BA-logos/logo_sq_header.png"), "dark": lambda request: static("logo_smartquailred.png")},
    "SITE_SYMBOL": "speed",
    "SITE_FAVICONS": [
        {
            "rel": "icon",
            "sizes": "32x28",
            "type": "image/svg+xml",
            "href": lambda request: static("img/SQLOGOS/smartbusinessanalytics.png"),
        },
    ],
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": True,
    "SHOW_BACK_BUTTON": True,
    "DASHBOARD_CALLBACK": "usuarios.views.dashboard_callback",
    "ENVIRONMENT": "qnd041app.utils.environment.environment_callback",
    "THEME": "light",
    "LOGIN": {  "image": lambda request: static("img/login_sq_bg.png"),
               "password_icon": lambda request: static("icons/eye-solid.svg"),
                "username_icon": lambda request: static("icons/username-icon.svg")
                },
    "LOGOUT": {  "image": lambda request: static("img/login_sq_bg.png"),
                },
               
    "STYLES": [
        lambda request: static("unfold/css/style.css"),        # archivo original
        lambda request: static("css/unfold_override.css"),     # tu override personalizado
    ],
    "SCRIPTS": [lambda request: static("unfold/js/script.js")],
    "BORDER_RADIUS": "6px",
    "COLORS": {
        "custom": {
            "green-success": "69 162 67",
            "red-alert": "69 162 67",
        },

        "base": {
            "50": "255 255 255",
            "100": "206 200 200",
            "200": "211 213 205",
            "300": "209 213 219",
            "400": "181 15 21",
            "500": "51 55 53",
            "600": "75 85 99",
            "700": "7 121 176",
            "800": "4 168 79",
            "900": "49 46 46",
            "950": "3 7 18",
        },
        "primary": {
            "50": "250 245 255",
            "100": "243 232 255",
            "200": "233 213 255",
            "300": "216 180 254",
            "400": "192 132 252",
            "500": "229 234 231",
            "600": "30 29 29",
            "700": "126 34 206",
            "800": "107 33 168",
            "900": "24 85 2",
            "950": "59 7 100",
            "750": "116, 132, 147",
        },
        "font": {
            "subtle-light": "var(--color-base-500)",
            "subtle-dark": "var(--color-base-400)",
            "default-light": "var(--color-base-600)",
            "default-dark": "var(--color-base-300)",
            "important-light": "var(--color-base-900)",
            "important-dark": "var(--color-base-100)",
        },
    },

    "TABS": [
        {
            "models": [{"name": "usuarios.prospecion_administrativa", "detail": True}],
            "items": [
                {
                    "title": _("Perfil Institucional"),
                    "link": reverse_lazy("admin:usuarios_prospecion_administrativa_changelist"),
                   # "permission": permission_callback,
                },
            ],
        },
    ],
    "SIDEBAR": {
        "show_search": False,
        "show_all_applications": False,
"navigation": [

    {
        "title": _("Recursos Legales (I+D)"),
        "separator": True,
        "collapsible": True,
        "items": [
            {
                "title": _(" Registros (SPDP)"),
                "icon": "create",
                "link": reverse_lazy("admin:smartbusinesslaw_spdp_actadelegado_changelist"),
                "badge": "usuarios.unfold_config.badge_callback_notificaciones",
                "badge_color": "custom-red-alert",
                "permission": is_all,
            },


            {
                "title": _("Balances (SCVS)"),
                "icon": "edit",
                "link": reverse_lazy("admin:smartbusinesslaw_scvsfinancialreport_changelist"),
                "badge": "usuarios.unfold_config.badge_callback_notificaciones",
                "badge_color": "custom-red-alert",
                "permission": is_all,
            },


            {
                "title": _("Informes (SCVS)"),
                "icon": "edit",
                "link": reverse_lazy("admin:smartbusinesslaw_scvs_actasasamblea_changelist"),
                "badge": "usuarios.unfold_config.badge_callback_notificaciones",
                "badge_color": "custom-red-alert",
                "permission": is_all,
            },


            {
                "title": _("Anexos (SRI)"),
                "icon": "edit",
                "link": reverse_lazy("admin:smartbusinesslaw_sri_anexostributarios_changelist"),
                "badge": "usuarios.unfold_config.badge_callback_notificaciones",
                "badge_color": "custom-red-alert",
                "permission": is_all,
            },


            {
                "title": _("Declaraciones (SRI)"),
                "icon": "edit",
                "link": reverse_lazy("admin:smartbusinesslaw_sri_declaracionimpuestos_changelist"),
                "badge": "usuarios.unfold_config.badge_callback_notificaciones",
                "badge_color": "custom-red-alert",
                "permission": is_all,
            },
            {
                "title": _("Contratos (MT)"),
                "icon": "signature",
                "link": reverse_lazy("admin:smartbusinesslaw_contratolaboral_changelist"),
                "badge": "usuarios.unfold_config.badge_callback_notificaciones",
                "badge_color": "custom-red-alert",
                "permission": is_all,
            },

            {
                "title": _("Nomina (IESS)"),
                "icon": "people",
                "link": reverse_lazy("admin:smartbusinesslaw_nomina_changelist"),
                "badge": "usuarios.unfold_config.badge_callback_notificaciones",
                "badge_color": "custom-red-alert",
                "permission": is_all,
            },

        ],
    },

    {
        "title": _("Recursos Financieros (I+D)"),
        "separator": True,
        "collapsible": True,
        "items": [

            {
                "title": _("Pasivos/Activos"),
                "icon": "folder",
                "link": reverse_lazy("admin:smartbusinessanalytics_id_activos_changelist"),
                "badge": "usuarios.unfold_config.badge_callback_notificaciones",
                "badge_color": "custom-red-alert",
                "permission": is_all,
            },


            {
                "title": _("Ingresos/Egresos"),
                "icon": "archive",
                "link": reverse_lazy("admin:smartbusinessanalytics_id_movimientofinanciero_changelist"),
                "badge": "usuarios.unfold_config.badge_callback_notificaciones",
                "badge_color": "custom-red-alert",
                "permission": is_all,
            },



            {
                    "title": _("Analisis Financieros"),
                    "icon": "analytics",
                    "link": reverse_lazy("admin:smartbusinessanalytics_id_estadofinanciero_changelist"),
                    "badge": "usuarios.unfold_config.badge_callback_analisis",
                    "badge_color": "custom-red-alert",
                    "permission": is_all,
        },

        ],
    },



],

    },
    "MENU": [
        #{"title": _("Dashboard"), "icon": "dashboard", "link": reverse_lazy("admin:index"), "permission": lambda request: request.user.is_superuser},
        {"title": _("Users"), "icon": "people", "link": reverse_lazy("admin:auth_user_changelist")},
        {
            "label": "Dashboard",
            "url": "/es/inicio/",
            "icon": "home",
        },
    ],
}







#LOGINGS REDIRECT

LOGIN_REDIRECT_URL = 'usuarios:perfil'
LOGIN_URL = 'login'
LOGOUT_URL = 'logout'


AUTH_USER_MODEL = 'usuarios.CustomUser'







PARLER_DEFAULT_LANGUAGE_CODE = 'es'
PARLER_DEFAULT_ACTIVATE = True
PARLER_SHOW_EXCLUDED_LANGUAGE_TABS = False



#AUTH_USER_MODEL = 'usuarios.Cita'


MIDDLEWARE = [
    #'django.contrib.sites.middleware.CurrentSiteMiddleware',
    'django.middleware.security.SecurityMiddleware',
   
    'django.contrib.sessions.middleware.SessionMiddleware',
    #'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.cache.FetchFromCacheMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.sites.middleware.CurrentSiteMiddleware',
    #'wagtail.core.middleware.site.SiteMiddleware',
    #'wagtail.contrib.redirects.middleware.RedirectMiddleware',
   # 'shop.middleware.LocaleRedirectMiddleware', 
]


LANGUAGE_CODE = 'es'

LOCALE_PATHS = [os.path.join(BASE_DIR, 'locale')]

TIME_ZONE = 'America/Guayaquil'  # O 'America/Mexico_City', 'America/Argentina/Buenos_Aires', etc.

USE_I18N = True
USE_L10N = True
USE_TZ = True


from django.utils.translation import gettext_lazy as _

LANGUAGES = [
    ('es', _('Español')),
    ('en', _('Inglés')),
]

ROOT_URLCONF = os.environ.get('ROOT_URLCONF')
#SITE_ID = 1
#WagtailAnalitycs



#WAGTAIL_SITE_NAME = os.environ.get('WAGTAIL_SITE_NAME ')

#RESTFRAMEWORK
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
    'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}






AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]





TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        "DIRS": [BASE_DIR /  "qnd041app","templates"], 
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
               # 'usuarios.context_processors.mensajes_nuevos_processor',
               # 'usuarios.context_processors.datos_panel_usuario', 
               # 'usuarios.context_processors.user_profile_data',
               # 'usuarios.context_processors.citas_context',
               # 'usuarios.context_processors.tareas_context',
               # 'usuarios.context_processors.pagos_context',  
               # 'usuarios.context_processors.profile_uploads_context',
               # 'usuarios.context_processors.ultima_cita',
               # 'usuarios.context_processors.ultima_tarea',
                'saas_cart.context_processors.cart',
                'paas_cart.context_processors.cart',
                "business_customer_projects.context_processors.business_projects_context",
                "business_customer_projects.context_processors.pending_payment_orders_total",
                "business_customer_projects.context_processors.noticias_context",
                "business_customer_projects.context_processors.tamano_empresa_context",
                "services_cart.context_processors.cart",

                'billing.context_processors.all_business_billing',
            ],
        },
    },
]

WSGI_APPLICATION = os.environ.get('WSGI_APPLICATION')










# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases


#POSTGRES_READY=str(os.environ.get('POSTGRES_READY_ENV'))





REDIS_HOST=os.environ.get('REDIS_HOST')
REDIS_PORT=os.environ.get('REDIS_PORT')
REDIS_DB =os.environ.get('REDIS_DB')  

CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL')
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_BACKEND = 'django-db'
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60 



# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# URL de tu webhook n8n
N8N_WEBHOOK_URL = "https://n8n.smartquail.io/webhook/social-post"
N8N_SECRET = "super-secret-key"



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/


MEDIA_URL = "/media/"
MEDIA_ROOT  = os.path.join(BASE_DIR, 'media')
STATICFILES_DIRS = [BASE_DIR / "staticfiles"]  
STATIC_URL = "/static/"
STATIC_ROOT = STATIC_ROOT = BASE_DIR / "static"





