

import os
from pathlib import Path
from dotenv import load_dotenv
from django.utils.translation import gettext_lazy as _
from django.templatetags.static import static
from django.urls import reverse_lazy
import json
import logging
from datetime import datetime
from django.urls import reverse_lazy
from decouple import config, Csv

#prueba
BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = os.environ.get('DEBUG')
# Load environment variables from the .env_local file.
ENV_FILE_PATH = BASE_DIR / ".env_stage"
load_dotenv(dotenv_path=ENV_FILE_PATH)

# Retrieve the Django secret key from environment variables.
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

SITE_ID = 1
domain = os.environ.get('SITE_DOMAIN', 'http://localhost:8000')

DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='support@smartquail.io')
SERVER_EMAIL = config('SERVER_EMAIL', default='support@smartquail.io')

CORS_ALLOWED_ORIGINS = [
    "https://ec.smartquail.io",  # ✅ Correcto
]


DATA_UPLOAD_MAX_NUMBER_FIELDS = None
#DEBUG = config('DEBUG', default=False, cast=bool)

#if DEBUG:
#    ADMINS = []
#else:
    # Obtener como lista separada por comas
#    raw_admins = config(
#        'ADMINS',
#        cast=Csv(),
#        default='Soporte SmartQuail:support@smartquail.io'
#    )

    # Transformar cada valor tipo 'Nombre:correo' en una tupla
#    ADMINS = [tuple(val.split(':')) for val in raw_admins]


# Optionally, you can add a default value or raise an exception if SECRET_KEY is not set
if SECRET_KEY is None:
    raise ValueError("DJANGO_SECRET_KEY is not set in the environment variables.")


class JSONLogFormatter(logging.Formatter):
    def format(self, record):
        timestamp = datetime.fromtimestamp(record.created).strftime('%Y-%m-%dT%H:%M:%S.%f')
        log_record = {
            "time": timestamp,
            "level": record.levelname,
            "name": record.name,
            "message": record.getMessage(),
        }
        return json.dumps(log_record)

SITE_DOMAIN = os.environ.get('SITE_DOMAIN', 'http://localhost:8000')

from usuarios.utils import permission_callback


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'json',
        },
    },

    'formatters': {
        'json': {
            'format': (
                '{"timestamp": "%(asctime)s", "level": "%(levelname)s", '
                '"logger": "%(name)s", "message": "%(message)s", '
                '"module": "%(module)s", "process": %(process)d, "thread": %(thread)d}'
            ),
        },
    },

    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },

    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

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

  
    "django.contrib.postgres",

    

    # Allauth core
    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    # Proveedores Sociales
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.github',
   

    "django.contrib.staticfiles",
    "django.contrib.humanize",
    'multiselectfield',
    'ai_agent',
    'building_admin',
    #'citas_regulares',
    #"core",
    #"wagtail_ai",
    "social_media_AI",
    "wagtail",
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    


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
    "wagtail.contrib.forms",

    # Wagtail plugins
    "wagtailgmaps",
    "wagtailmenus",

    # "wagtail_modeltranslation",  # Descomentar si se usa
    'import_export',
    # Terceros / externos
    "rest_framework",
    #"ckeditor",
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
    #"bootstrap4",
    #"bootstrap5",
    #"bootstrap_datepicker_plus",
    "jquery",
    "qr_code",
    "tinymce",
    "phone_field",
    "phonenumber_field",
    "django_social_share",
    "business_customer_projects",
    'smartbusinesslaw',
    'smartbusinesslaw_demo',
    'smartbusinessanalytics_id',
    'smartbusinessanalytics_demo',

             # Apps propias del proyecto
    "usuarios",
    #'businees_customers_projects',
    #"SQOrders",
    #"SQShop",
    'chatbot_ai',

   
    "webapp",
    "serviceapp",
    'billing',
    #"citas_regulares",

    # E-commerce apps
    "cloudcalc",
    #"coupons",
    'iaas_shop',
    'iaas_cart',
    'iaas_orders',
    'iaas_coupons',
    'iaas_payment',
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

        #AIAAS
    'aiaas_shop',
    'aiaas_orders',
    'aiaas_cart',
    'aiaas_coupons',
    'aiaas_payment',

    #SmartBusinessANALYTICS
    "sbacart",
    "sbashop",
    "sbaorders",
    #SmartBusinessLaw
    "sblcart",
    "sblshop",
    "sblorders",
    'sbpshop',

    #'mailing',

    "customer_managemen",

    #SmartBusinessTechonologies
    "sbtcart",
    "sbtshop",
    "sbtorders",
    #SmartBusinessMedia
    "sbmcart",
    "sbmshop",
    "sbmorders",
    "sbmcoupons",
    "sbmpayments",
    "whatsappbot",
    #"sbacart",
    #"sbashop",
    #"sbaorders",
    "services_cart",
    "services_coupons",
    "services_payment",
    "rosetta",
    "taggit",
    'studio_leads_ai',
    'wagtail.contrib.sitemaps',
    "social_media_A",
    'corsheaders',
    'wagtail_analytics',
    'django.contrib.sitemaps',
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
AIAAS_CART_SESSION_ID = 'aiaas_cart'

SERVICES_CART_SESSION_ID = 'services_cart'


from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


def badge_color_callback(request):
    count = 1
    if count == 0:
        return "info"
    elif count < 2:
        return "info"
    return "info"


def _in_group(request, group_name):
    user = getattr(request, "user", None)
    if not user or not user.is_authenticated:
        return False
    return user.groups.filter(name=group_name).exists()


def is_terapeuta(request):
    return _in_group(request, "terapeutico")


def is_administrativo(request):
    return _in_group(request, "administrativo")


def is_financiero(request):
    return _in_group(request, "financiero")


def is_institucional(request):
    return _in_group(request, "institucional")


def is_superuser(request):
    user = getattr(request, "user", None)
    return bool(user and user.is_authenticated and user.is_superuser)


def is_administrativo_o_isuperuser(request):
    return is_administrativo(request) or is_superuser(request)


def is_institucional_o_terapeuta_o_administrativo(request):
    return (
        is_institucional(request)
        or is_terapeuta(request)
        or is_administrativo(request)
        or is_superuser(request)
    )


def is_institucional_o_administrativo(request):
    return is_institucional(request) or is_administrativo(request) or is_superuser(request)


def is_admin_o_terapeuta(request):
    return is_administrativo(request) or is_terapeuta(request) or is_superuser(request)


def is_admin_o_financiero(request):
    return is_administrativo(request) or is_financiero(request) or is_superuser(request)


def is_staff_activo(request):
    """
    Filtro de seguridad I+D: Verifica que el usuario sea
    miembro del staff autorizado y su cuenta esté activa.
    """
    user = getattr(request, "user", None)
    return bool(
        user
        and user.is_authenticated
        and user.is_staff
        and user.is_active
    )


def is_all(request):
    """
    Control de acceso total a la Suite. Permite la visualización si cumple
    con los roles específicos del holding O si es un usuario Staff Activo.
    """
    return (
        is_staff_activo(request)
        or is_administrativo(request)
        or is_financiero(request)
        or is_superuser(request)
        or is_terapeuta(request)
        or is_institucional(request)
    )


UNFOLD = {
    "SITE_TITLE": "SmartQuail IT Cloud Business (I+D)® - Entornos Operativos, Financieros y Edificios",
    "SITE_SUB_TITLE": "Procesos Analíticos, Legales y Gestión de Edificios",
    "SITE_HEADER": "SmartQuail Cloud Business",
    "SITE_SUBHEADER": "by SmartQuail, Inc.",
    "SITE_VERSION": "1.0.1",
    "SITE_DESCRIPTION": "SmartQuail® es un sistema de gestión operativa, financiera, legal y de administración de edificios diseñado para entornos críticos y cumplimiento normativo.",
    "SITE_COPYRIGHT": "Copyright © 2026 SmartQuail S.A.S Todos los derechos reservados.",
    "DASHBOARD_CALLBACK": "usuarios.views.dashboard_callback",
    "ENVIRONMENT": "qnd041app.utils.environment.environment_callback",
    "SHOW_LANGUAGES": False,
    "LOGIN": {
        "image": lambda request: static("img/login_sq_bg.png"),
        "password_icon": lambda request: static("icons/eye-solid.svg"),
        "username_icon": lambda request: static("icons/username-icon.svg"),
        "redirect_after": lambda request: reverse_lazy("admin:index"),
    },
    "LOGOUT": {
        "image": lambda request: static("img/login_sq_bg.png"),
    },
    "SITE_DROPDOWN": [
        {
            "icon": "person",
            "title": _("Usuarios (AUTH)"),
            "link": reverse_lazy("admin:auth_user_changelist"),
        },
        {
            "icon": "key",
            "title": _("Roles (RBAC)"),
            "link": reverse_lazy("admin:auth_group_changelist"),
        },
        {
            "icon": "map",
            "title": _("Regulaciones"),
            "link": reverse_lazy("admin:smartbusinesslaw_regulacion_changelist"),
        },
        {
            "icon": "circle",
            "title": _("Monitoreo"),
            "link": reverse_lazy("admin:django_celery_results_taskresult_changelist"),
        },
        {
            "icon": "support",
            "title": _("Soporte"),
            "link": reverse_lazy("admin:usuarios_cliente_changelist"),
        },
    ],
    "SITE_URL": "https://ec.smartquail.io",
    "SITE_SYMBOL": "apartment",
    "SITE_ICON": {
        "light": lambda request: static("img/BA-LOGOS/loro.png"),
        "dark": lambda request: static("img/BA-LOGOS/loro.png"),
    },
    "SITE_LOGO": {
        "light": lambda request: static("img/BA-LOGOS/logo_sq_header.png"),
        "dark": lambda request: static("logo_smartquailred.png"),
    },
    "SITE_FAVICONS": [
        {
            "rel": "icon",
            "sizes": "32x32",
            "type": "image/png",
            "href": lambda request: static("img/PRODUCT_LOGOS/logo_red_user.png"),
        },
    ],
    "STYLES": [
        lambda request: static("unfold/css/style.css"),
        lambda request: static("css/unfold_override.css"),
    ],
    "SCRIPTS": [
        lambda request: static("unfold/js/script.js"),
    ],
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": True,
    "SHOW_BACK_BUTTON": True,
    "SHOW_UI_WARNINGS": True,
    "USER_DROPDOWN": [
        {
            "title": _("Cambiar contraseña"),
            "icon": "key",
            "link": lambda request: reverse_lazy("admin:password_change"),
        },
        {
            "title": _("Cerrar sesión"),
            "icon": "logout",
            "link": lambda request: reverse_lazy("admin:logout"),
        },
    ],
    "BORDER_RADIUS": "7px",
    "COLORS": {
        "custom": {
            "green-success": "69 162 67",
            "red-alert": "181 15 21",
        },
        "base": {
            "50": "oklch(98.5% .002 247.839)",
            "100": "oklch(95% .003 264.542)",
            "200": "oklch(88% .005 264.531)",
            "300": "oklch(75% .008 258.338)",
            "400": "oklch(55% .012 261.325)",
            "500": "oklch(40% .015 264.364)",
            "600": "oklch(30% .018 256.802)",
            "700": "oklch(22% .02 259.733)",
            "800": "oklch(16% .022 256.848)",
            "900": "oklch(11% .025 264.665)",
            "950": "oklch(7% .02 261.692)",
        },
        "primary": {
            "50": "oklch(97% .02 20.0)",
            "100": "oklch(92% .05 20.0)",
            "200": "oklch(84% .10 20.0)",
            "300": "oklch(73% .16 20.0)",
            "400": "oklch(62% .22 25.0)",
            "500": "oklch(53% .25 27.0)",
            "600": "oklch(46% .23 27.0)",
            "700": "oklch(39% .20 27.0)",
            "800": "oklch(33% .17 27.0)",
            "900": "oklch(27% .14 27.0)",
            "950": "oklch(18% .10 27.0)",
        },
        "font": {
            "subtle-light": "var(--color-base-500)",
            "subtle-dark": "var(--color-base-400)",
            "default-light": "var(--color-base-700)",
            "default-dark": "var(--color-base-200)",
            "important-light": "var(--color-base-950)",
            "important-dark": "var(--color-base-50)",
        },
    },
    "TABS": [
        {
            "models": [
                {"name": "usuarios.prospecion_administrativa", "detail": True},
                "sba.estadofinanciero",
                "sba.movimientofinanciero",
                "sba.sesioncaja",
                "sba.transaccioncaja",
                "building_admin.edificio",
                "building_admin.unidad",
                "building_admin.cargoalicuota",
            ],
            "items": [
                {
                    "title": _("Panel Ejecutivo"),
                    "link": reverse_lazy("admin:index"),
                },
                {
                    "title": _("Perfil Institucional"),
                    "link": reverse_lazy("admin:usuarios_prospecion_administrativa_changelist"),
                },
            ],
        },
    ],
    "SIDEBAR": {
        "show_search": False,
        "show_all_applications": False,
        "navigation": [
            {
                "title": _("Administración de Edificios"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Edificios"),
                        "icon": "apartment",
                        "link": reverse_lazy("admin:building_admin_edificio_changelist"),
                        "permission": is_all,
                    },
                    {
                        "title": _("Áreas Comunes"),
                        "icon": "meeting_room",
                        "link": reverse_lazy("admin:building_admin_areacomun_changelist"),
                        "permission": is_all,
                    },
                    {
                        "title": _("Registro de Limpieza"),
                        "icon": "cleaning_services",
                        "link": reverse_lazy("admin:building_admin_registrolimpieza_changelist"),
                        "permission": is_all,
                    },
                    {
                        "title": _("Órdenes de Mantenimiento"),
                        "icon": "engineering",
                        "link": reverse_lazy("admin:building_admin_ordenmantenimiento_changelist"),
                        "permission": is_all,
                    },
                    {
                        "title": _("Unidades"),
                        "icon": "domain",
                        "link": reverse_lazy("admin:building_admin_unidad_changelist"),
                        "permission": is_all,
                    },
                    {
                        "title": _("Cargos y Alícuotas"),
                        "icon": "receipt_long",
                        "link": reverse_lazy("admin:building_admin_cargoalicuota_changelist"),
                        "permission": is_all,
                    },
                    {
                        "title": _("Documentos Normativos"),
                        "icon": "gavel",
                        "link": reverse_lazy("admin:building_admin_documentonormativo_changelist"),
                        "permission": is_all,
                    },
                    {
                        "title": _("Fragmentos Normativos"),
                        "icon": "article",
                        "link": reverse_lazy("admin:building_admin_fragmentonormativo_changelist"),
                        "permission": is_all,
                    },
                ],
            },
            {
                "title": _("Recursos Legales (I+D)"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Registros (SPDP)"),
                        "icon": "create",
                        "link": reverse_lazy("admin:smartbusinesslaw_spdp_actadelegado_changelist"),
                        "badge": "usuarios.unfold_config.badge_callback_notificaciones",
                        "badge_color": "custom-red-alert",
                        "permission": is_all,
                    },
                    {
                        "title": _("Nombramientos (SCVS)"),
                        "icon": "edit",
                        "link": reverse_lazy("admin:smartbusinesslaw_cartanombramiento_changelist"),
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
                        "title": _("Ingresos Mensuales"),
                        "icon": "folder",
                        "link": reverse_lazy("admin:business_customer_projects_paymentorder_changelist"),
                        "badge": "usuarios.unfold_config.badge_callback_notificaciones",
                        "badge_color": "custom-red-alert",
                        "permission": is_all,
                    },
                    {
                        "title": _("Ordenes (SaaP)"),
                        "icon": "folder",
                        "link": reverse_lazy("admin:saas_orders_saasorder_changelist"),
                        "badge": "usuarios.unfold_config.badge_callback_notificaciones",
                        "badge_color": "custom-red-alert",
                        "permission": is_all,
                    },
                    {
                        "title": _("Ordenes (PaaP)"),
                        "icon": "folder",
                        "link": reverse_lazy("admin:paas_orders_paasorder_changelist"),
                        "badge": "usuarios.unfold_config.badge_callback_notificaciones",
                        "badge_color": "custom-red-alert",
                        "permission": is_all,
                    },
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
            {
                "title": _("Gestor administrativo & legal"),
                "separator": False,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Registros (SPDP)"),
                        "icon": "create",
                        "link": reverse_lazy("admin:smartbusinesslaw_demo_spdp_actadelegado_changelist"),
                        "badge": "usuarios.unfold_config.badge_callback_notificaciones",
                        "badge_color": "custom-red-alert",
                        "permission": is_staff_activo,
                    },
                    {
                        "title": _("Balances (SCVS)"),
                        "icon": "edit",
                        "link": reverse_lazy("admin:smartbusinesslaw_demo_scvsfinancialreport_changelist"),
                        "badge": "usuarios.unfold_config.badge_callback_notificaciones",
                        "badge_color": "custom-red-alert",
                        "permission": is_staff_activo,
                    },
                    {
                        "title": _("Informes (SCVS)"),
                        "icon": "edit",
                        "link": reverse_lazy("admin:smartbusinesslaw_demo_scvs_actasasamblea_changelist"),
                        "badge": "usuarios.unfold_config.badge_callback_notificaciones",
                        "badge_color": "custom-red-alert",
                        "permission": is_staff_activo,
                    },
                    {
                        "title": _("Anexos (SRI)"),
                        "icon": "edit",
                        "link": reverse_lazy("admin:smartbusinesslaw_demo_sri_anexostributarios_changelist"),
                        "badge": "usuarios.unfold_config.badge_callback_notificaciones",
                        "badge_color": "custom-red-alert",
                        "permission": is_staff_activo,
                    },
                    {
                        "title": _("Declaraciones (SRI)"),
                        "icon": "edit",
                        "link": reverse_lazy("admin:smartbusinesslaw_demo_sri_declaracionimpuestos_changelist"),
                        "badge": "usuarios.unfold_config.badge_callback_notificaciones",
                        "badge_color": "custom-red-alert",
                        "permission": is_staff_activo,
                    },
                    {
                        "title": _("Contratos (MT)"),
                        "icon": "signature",
                        "link": reverse_lazy("admin:smartbusinesslaw_demo_contratolaboral_changelist"),
                        "badge": "usuarios.unfold_config.badge_callback_notificaciones",
                        "badge_color": "custom-red-alert",
                        "permission": is_staff_activo,
                    },
                ],
            },
            {
                "title": _("Gestor Financiero & Analítico"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Activos/Pasivos"),
                        "icon": "folder",
                        "link": reverse_lazy("admin:smartbusinessanalytics_demo_activos_changelist"),
                        "badge": "smartbusinessanalytics_demo.unfold_config.badge_callback_activos",
                        "badge_color": "custom-red-alert",
                        "permission": is_staff_activo,
                    },
                    {
                        "title": _("Ingresos/Egresos"),
                        "icon": "archive",
                        "link": reverse_lazy("admin:smartbusinessanalytics_demo_movimientofinanciero_changelist"),
                        "badge": "smartbusinessanalytics_demo.unfold_config.badge_callback_ingresos_egresos",
                        "badge_color": "custom-red-alert",
                        "permission": is_staff_activo,
                    },
                    {
                        "title": _("Resultados"),
                        "icon": "analytics",
                        "link": reverse_lazy("admin:smartbusinessanalytics_demo_estadofinanciero_changelist"),
                        "badge": "smartbusinessanalytics_demo.unfold_config.badge_callback_notificaciones",
                        "badge_color": "custom-red-alert",
                        "permission": is_staff_activo,
                    },
                ],
            },
            {
                "title": _("Project Management (I+D)"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Actividades"),
                        "icon": "folder",
                        "link": reverse_lazy("admin:usuarios_registroactividad_changelist"),
                        "badge": "usuarios.unfold_config.badge_callback_notificaciones",
                        "badge_color": "custom-red-alert",
                        "permission": is_all,
                    },
                    {
                        "title": _("Clientes ITC"),
                        "icon": "people",
                        "link": reverse_lazy("admin:usuarios_profile_changelist"),
                        "badge": "usuarios.unfold_config.badge_callback_notificaciones",
                        "badge_color": "custom-red-alert",
                        "permission": is_all,
                    },
                    {
                        "title": _("Proyectos ITC"),
                        "icon": "folder",
                        "link": reverse_lazy("admin:business_customer_projects_businesssystemproject_changelist"),
                        "badge": "usuarios.unfold_config.badge_callback_notificaciones",
                        "badge_color": "custom-red-alert",
                        "permission": is_all,
                    },
                    {
                        "title": _("Recursos ITC"),
                        "icon": "folder",
                        "link": reverse_lazy("admin:business_customer_projects_monthlysystemmetrics_changelist"),
                        "badge": "usuarios.unfold_config.badge_callback_notificaciones",
                        "badge_color": "custom-red-alert",
                        "permission": is_all,
                    },
                    {
                        "title": _("DeV (I+D) ITC"),
                        "icon": "folder",
                        "link": reverse_lazy("admin:business_customer_projects_businessprocess_changelist"),
                        "badge": "usuarios.unfold_config.badge_callback_notificaciones",
                        "badge_color": "custom-red-alert",
                        "permission": is_all,
                    },
                ],
            },
            {
                "title": _("Develop Management (I+D)"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Quantity Testing"),
                        "icon": "folder",
                        "link": reverse_lazy("admin:business_customer_projects_qatest_changelist"),
                        "permission": is_all,
                    },
                    {
                        "title": _("Cloud Resources"),
                        "icon": "folder",
                        "link": reverse_lazy("admin:business_customer_projects_cloudresource_changelist"),
                        "permission": is_all,
                    },
                    {
                        "title": _("Investigación & Desarollo"),
                        "icon": "folder",
                        "link": reverse_lazy("admin:business_customer_projects_businessprocess_changelist"),
                        "permission": is_all,
                    },
                    {
                        "title": _("Automatizaciones"),
                        "icon": "folder",
                        "link": reverse_lazy("admin:business_customer_projects_businessautomation_changelist"),
                        "permission": is_all,
                    },
                    {
                        "title": _("Inteligencia Artificial"),
                        "icon": "folder",
                        "link": reverse_lazy("admin:business_customer_projects_businessintelligent_changelist"),
                        "permission": is_all,
                    },
                ],
            },
            {
                "title": _("Product Management (I+D)"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Categorías (SaaP)"),
                        "icon": "folder",
                        "link": reverse_lazy("admin:saas_shop_category_changelist"),
                        "permission": is_all,
                    },
                    {
                        "title": _("Productos (SaaP)"),
                        "icon": "folder",
                        "link": reverse_lazy("admin:saas_shop_product_changelist"),
                        "permission": is_all,
                    },
                    {
                        "title": _("Categorías (PaaP)"),
                        "icon": "folder",
                        "link": reverse_lazy("admin:paas_shop_category_changelist"),
                        "permission": is_all,
                    },
                    {
                        "title": _("Productos (PaaP)"),
                        "icon": "folder",
                        "link": reverse_lazy("admin:paas_shop_product_changelist"),
                        "permission": is_all,
                    },
                    {
                        "title": _("Categorías (AIaaP)"),
                        "icon": "folder",
                        "link": reverse_lazy("admin:aiaas_shop_category_changelist"),
                        "permission": is_all,
                    },
                    {
                        "title": _("Productos (AIaaP)"),
                        "icon": "folder",
                        "link": reverse_lazy("admin:aiaas_shop_product_changelist"),
                        "permission": is_all,
                    },
                    {
                        "title": _("Categorías (IaaP)"),
                        "icon": "folder",
                        "link": reverse_lazy("admin:iaas_shop_category_changelist"),
                        "permission": is_all,
                    },
                    {
                        "title": _("Productos (IaaP)"),
                        "icon": "folder",
                        "link": reverse_lazy("admin:iaas_shop_product_changelist"),
                        "permission": is_all,
                    },
                ],
            },
            {
                "title": _("Catalogos de Productos (Web)"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Categorías SBM"),
                        "icon": "folder",
                        "link": reverse_lazy("admin:sbmshop_category_changelist"),
                        "permission": is_all,
                    },
                    {
                        "title": _("Categorías SBA"),
                        "icon": "folder",
                        "link": reverse_lazy("admin:sbashop_category_changelist"),
                        "permission": is_all,
                    },
                    {
                        "title": _("Categorías SBL"),
                        "icon": "folder",
                        "link": reverse_lazy("admin:sblshop_category_changelist"),
                        "permission": is_all,
                    },
                    {
                        "title": _("Categorías SBT"),
                        "icon": "folder",
                        "link": reverse_lazy("admin:sbtshop_category_changelist"),
                        "permission": is_all,
                    },
                    {
                        "title": _("Productos SBM"),
                        "icon": "folder",
                        "link": reverse_lazy("admin:sbmshop_sbmproduct_changelist"),
                        "permission": is_all,
                    },
                    {
                        "title": _("Productos SBA"),
                        "icon": "folder",
                        "link": reverse_lazy("admin:sbashop_sbaproduct_changelist"),
                        "permission": is_all,
                    },
                    {
                        "title": _("Productos SBL"),
                        "icon": "folder",
                        "link": reverse_lazy("admin:sblshop_sblproduct_changelist"),
                        "permission": is_all,
                    },
                    {
                        "title": _("Productos SBT"),
                        "icon": "folder",
                        "link": reverse_lazy("admin:sbtshop_sbtproduct_changelist"),
                        "permission": is_all,
                    },
                ],
            },
            {
                "title": _("Ebooks ITC"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Ebook Categorías"),
                        "icon": "folder",
                        "link": reverse_lazy("admin:business_customer_projects_categorianoticia_changelist"),
                        "badge": "usuarios.unfold_config.badge_callback_notificaciones",
                        "badge_color": "custom-red-alert",
                        "permission": is_all,
                    },
                    {
                        "title": _("Crear Ebook"),
                        "icon": "folder",
                        "link": reverse_lazy("admin:business_customer_projects_noticia_changelist"),
                        "badge": "usuarios.unfold_config.badge_callback_notificaciones",
                        "badge_color": "custom-red-alert",
                        "permission": is_all,
                    },
                ],
            },
        ],
    },
}











MIDDLEWARE = [
    #'django.contrib.sites.middleware.CurrentSiteMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.sites.middleware.CurrentSiteMiddleware',
    #'elasticapm.contrib.django.middleware.TracingMiddleware'
    #'wagtail.core.middleware.site.SiteMiddleware',
    #'wagtail.contrib.redirects.middleware.RedirectMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

#ELASTIC_APM = {
    #'SERVICE_NAME': 'qnd031app',
    #'SECRET_TOKEN': '',  # déjalo vacío si no usas auth
    #'SERVER_URL': 'http://apm-server:8200',
    #'ENVIRONMENT': 'production',
    #'DEBUG': True,
#}




ROOT_URLCONF = os.environ.get('ROOT_URLCONF')


REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ]
}


#Redis Setup




#DJANGO ADMIN SETUPS

#LOGINGS REDIRECT

LOGIN_REDIRECT_URL = 'usuarios:perfil'
LOGIN_URL = 'login'
LOGOUT_URL = 'logout'

#from django.urls import reverse_lazy
#LOGIN_REDIRECT_URL = reverse_lazy('course_list')

# Configuración de sesiones usando Redis
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"
REDIS_HOST = os.environ.get('REDIS_HOST')  # Cambia esto según tu configuración
REDIS_PORT  = os.environ.get('REDIS_PORT')        # Puerto por defecto de Redis
REDIS_DB  = os.environ.get('REDIS_DB')

#WEBAPP SETTINGS



EMAIL_BACKEND = config("EMAIL_BACKEND")
EMAIL_HOST = config("EMAIL_HOST")
EMAIL_PORT = config("EMAIL_PORT", cast=int)
EMAIL_USE_TLS = config("EMAIL_USE_TLS", cast=bool)
EMAIL_USE_SSL = config("EMAIL_USE_SSL", cast=bool)
EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_HOST_USER_INFO = config("EMAIL_HOST_USER_INFO", default="info@tudominio.com")
EMAIL_HOST_USER_LICENCIAS = config("EMAIL_HOST_USER_LICENCIAS", default="licencias@tudominio.com")
EMAIL_HOST_USER_ACTIVOS = config("EMAIL_HOST_USER_ACTIVOS", default="licencias@tudominio.com")
EMAIL_HOST_USER_CTO = config("EMAIL_HOST_USER_CTO", default="licencias@tudominio.com")


EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
DEFAULT_FROM_EMAIL_LICENCIAS = EMAIL_HOST_USER_LICENCIAS 
DEFAULT_FROM_EMAIL_INFO = EMAIL_HOST_USER_INFO
DEFAULT_FROM_EMAIL_ACTIVOS  = EMAIL_HOST_USER_ACTIVOS 
DEFAULT_FROM_EMAIL_CTO = EMAIL_HOST_USER_CTO 



CART_SESSION_ID = 'cart'
SBLCART_SESSION_ID = 'cart'
SBACART_SESSION_ID = 'cart'
SBTCART_SESSION_ID = 'cart'
SBMCART_SESSION_ID = 'cart'

BRAINTREE_MERCHANT_ID = os.environ.get('BRAINTREE_M_ID')
BRAINTREE_PUBLIC_KEY = os.environ.get('BRAINTREE_KEY')
BRAINTREE_PRIVATE_KEY = os.environ.get('BRAINTREE_PRIVATE_KEY')

from braintree import Configuration, Environment
# para desplegar cambiar sandbox con Production
Configuration.configure(
    Environment.Sandbox,
    BRAINTREE_MERCHANT_ID,
    BRAINTREE_PUBLIC_KEY,
    BRAINTREE_PRIVATE_KEY
)



AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    #'account.authentication.EmailAuthBackend',
    #'social_core.backends.facebook.FacebookOAuth2',
    #'social_core.backends.twitter.TwitterOAuth',
    #'social_core.backends.google.GoogleOAuth2',
    # Login tradicional de Django (superusuario / contraseña)
    # Backend de autenticación de Allauth
    'allauth.account.auth_backends.AuthenticationBackend',
]


# ==============================================================================
# CONFIGURACIÓN DJANGO-ALLAUTH & ACCOUNT AUTHENTICATION
# ==============================================================================

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'optional'
ACCOUNT_USER_MODEL_USERNAME_FIELD = None

# Automatización de registro social sin pantallas intermedias
SOCIALACCOUNT_AUTO_SIGNUP = True 
SOCIALACCOUNT_EMAIL_AUTHENTICATION_AUTO_CONNECT = True

# ==============================================================================
# CONFIGURACIÓN DE SCOPES / PERMISOS PARA PROVEEDORES SOCIALES
# ==============================================================================
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    },
    'facebook': {
        'METHOD': 'oauth2',
        'SCOPE': ['email', 'public_profile'],
        'FIELDS': [
            'id',
            'email',
            'name',
            'first_name',
            'last_name',
        ],
        'EXCHANGE_TOKEN': True,
        'VERSION': 'v18.0',
    },
    'github': {
        'SCOPE': [
            'user',
            'user:email',
        ],
    }
}



AUTH_USER_MODEL = 'usuarios.CustomUser'


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
                "wagtail.contrib.settings.context_processors.settings",

            ],
        },
    },
]

WSGI_APPLICATION = os.environ.get('WSGI_APPLICATION')

WAGTAIL_ADMIN_BASE_URL =  os.environ.get('DOMAINS')
WAGTAILIMAGES_MAX_UPLOAD_SIZE = 5 * 1024 * 1024 * 1024  # 5 GB en bytes
WAGTAILIMAGES_MAX_IMAGE_PIXELS = 1000000000  # 1 millardo de píxeles (1 Gb)



WAGTAIL_AI = {
    "BACKENDS": {
        "gemini": {
            "CLASS": "qnd041app.settings.gemini_backend.GeminiBackend",
            "CONFIG": {
                "MODEL_ID": "gemini-1.5-flash",  # rápido/barato
                # también puedes usar:
                # gemini-1.5-pro → más potente
                "API_KEY": os.environ.get("GEMINI_API_KEY"),
            },
        },
    },
    "TEXT_COMPLETION_BACKEND": "gemini",
}


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases


#POSTGRES_READY=str(os.environ.get('POSTGRES_READY_ENV'))





# Configuración de sesiones usando Redis
#SESSION_ENGINE = "django.contrib.sessions.backends.cache"
#SESSION_CACHE_ALIAS = "default"




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


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/



LOCALE_PATHS = [os.path.join(BASE_DIR, 'locale')]

TIME_ZONE = 'America/Guayaquil'  # O 'America/Mexico_City', 'America/Argentina/Buenos_Aires', etc.
LANGUAGE_CODE = 'es'

WAGTAIL_ADMIN_BASE_URL = 'https://ec.smartquail.io'

WAGTAIL_SITE_NAME = "Smart Business MEDIA"
WAGTAIL_CONTENT_LANGUAGES = LANGUAGES = [
    ('en', 'English'),
    ('es', 'Spanish'),
]

LANGUAGE_CODE = 'es'


WAGTAIL_I18N_ENABLED = False

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

USE_I18N = False
USE_L10N = False
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/



# Rutas públicas a los archivos
#MEDIA_URL = "https://www-static.sfo3.digitaloceanspaces.com/media/"
#STATIC_URL = "https://www-static.sfo3.digitaloceanspaces.com/static/"
