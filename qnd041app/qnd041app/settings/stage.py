from .base_stage import *






ENV_FILE_PATH = BASE_DIR / ".env_stage"
load_dotenv(str(ENV_FILE_PATH))

DEBUG=os.environ.get("DEBUG")

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(",") if os.environ.get("ALLOWED_HOSTS") else []




#import wagtail_ai

#WAGTAIL_AI_PROMPTS = wagtail_ai.DEFAULT_PROMPTS + [
#    {
#        "label": "Simplify",
#        "description": "Rewrite your text in a simpler form",
#        "prompt": "Rewrite the following text to make it simper and more succinct",
#        "method": "replace",
#    }
#]


#CSRF_COOKIE_DOMAIN=".www.smartquail.io"
#CSRF_COOKIE_SECURE = True
#CSRF_TRUSTED_ORIGINS = ['https://www.smartquail.io','https://146.190.164.22']
#CORS_ALLOWED_ORIGINS = [
#    'https://www.smartquail.io','https://146.190.164.22'
    # Otros orígenes permitidos si los hay
#]





DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Obtención de variables de entorno para la configuración de PostgreSQL
DB_USERNAME = os.environ.get("POSTGRES_USER")
DB_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
DB_DATABASE = os.environ.get("POSTGRES_DB")
DB_HOST = os.environ.get("POSTGRES_HOST")
DB_PORT = os.environ.get("POSTGRES_PORT")
DB_ENGINE = os.environ.get("POSTGRES_ENGINE")

# Verificación de disponibilidad de las variables necesarias para PostgreSQL
DB_IS_AVAILABLE = all([
    DB_USERNAME,
    DB_PASSWORD,
    DB_DATABASE,
    DB_HOST,
    DB_PORT
])

# Configuración condicional para PostgreSQL
if DB_IS_AVAILABLE:
    DATABASES = {
        'default': {
            'ENGINE': DB_ENGINE,
            'NAME': DB_DATABASE,
            'USER': DB_USERNAME,
            'PASSWORD': DB_PASSWORD,
            'HOST': DB_HOST,
            'PORT': DB_PORT,
        }
    }

#Static files DevMod


CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'height': 300,
        'width': '100%',
    },
}

# settings.py

DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# celery setup

# celery setup


Q_CLUSTER = {
   'name': 'DjangORM',
   'workers': 4,
   'timeout': 90,
   'retry': 120,
   'queue_limit': 50,
   'bulk': 10,
   'orm': 'default',
}
USE_DJANGO_Q_FOR_EMAILS = True


CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# Configuración del broker y serialización en Celery
CELERY_BROKER_URL = 'pyamqp://guest:guest@localhost//'
CELERY_RESULT_BACKEND = 'django-db'
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60 


# Configuración de serialización actualizada (según las advertencias)
accept_content = ['json']  # Esto reemplaza 'CELERY_ACCEPT_CONTENT'
task_serializer = 'json'   # Esto reemplaza 'CELERY_TASK_SERIALIZER'
result_serializer = 'json'  # Esto reemplaza 'CELERY_RESULT_SERIALIZER'

# Si deseas mantener el comportamiento de reconexión automática en el inicio del broker, usa:
#broker_connection_retry_on_startup = True


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

EMAIL_HOST = 'smtp.gmail.com'  # Para Gmail
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'phys.mauricio.silva@gmail.com'  # Tu correo de Gmail
EMAIL_HOST_PASSWORD = '1719183830'  # La contraseña de tu cuenta de Gmail
DEFAULT_FROM_EMAIL = 'phys.mauricio.silva@gmail.com'




TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_FROM = os.getenv("TWILIO_WHATSAPP_FROM")