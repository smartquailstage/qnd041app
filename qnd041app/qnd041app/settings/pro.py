from .base_prod import *

# Obtener las variables de entorno desde Kubernetes
IP = os.environ.get("IP")
DOMAIN = os.environ.get("DOMAIN")
HOST = os.environ.get("HOST")

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'https://ec.smartquail.io', 'ec.smartquail.io', '64.23.178.103']

CORS_ALLOWED_ORIGINS = [
    'https://ec.smartquail.io',
    'ec.smartquail.io'
]

# Base de datos por defecto (SQLite de respaldo si no hay PostgreSQL)
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

DB_IS_AVAILABLE = all([
    DB_USERNAME,
    DB_PASSWORD,
    DB_DATABASE,
    DB_HOST,
    DB_PORT
])

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

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Celery setup
REDIS_HOST = os.environ.get('REDIS_HOST')
REDIS_PORT = os.environ.get('REDIS_PORT')
REDIS_DB = os.environ.get('REDIS_DB')

CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL')
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_BACKEND = 'django-db'
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30

CELERY_BEAT_SCHEDULE = {
    'deactivate_old_orders': {
        'task': 'saas_orders.tasks.deactivate_old_orders',
        'schedule': 86400.0,
    },
}

# Social auth settings
SOCIAL_AUTH_FACEBOOK_KEY = os.environ.get('SOCIAL_AUTH_FACEBOOK_KEY')
SOCIAL_AUTH_FACEBOOK_SECRET = os.environ.get('SOCIAL_AUTH_FACEBOOK_SECRET')
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']

SOCIAL_AUTH_TWITTER_KEY = os.environ.get('SOCIAL_AUTH_TWITTER_KEY')
SOCIAL_AUTH_TWITTER_SECRET = os.environ.get('SOCIAL_AUTH_TWITTER_SECRET')

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.environ.get('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.environ.get('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')

def env(key, default=None):
    return os.getenv(key, default)

N8N_WEBHOOKS_A = {
    "instagram_post": env("N8N_A_INSTAGRAM_POST"),
    "instagram_carousel": env("N8N_A_INSTAGRAM_CAROUSEL"),
    "instagram_reel": env("N8N_A_INSTAGRAM_REEL"),
    "facebook_image": env("N8N_A_FACEBOOK_IMAGE"),
    "facebook_video": env("N8N_A_FACEBOOK_VIDEO"),
    "facebook_carousel": env("N8N_A_FACEBOOK_CAROUSEL"),
    "twitter_post": env("N8N_A_TWITTER_POST"),
    "linkedin_post": env("N8N_A_LINKEDIN_POST"),
}

N8N_WEBHOOKS_AI = {
    "instagram_post": env("N8N_AI_INSTAGRAM_POST"),
    "instagram_carousel": env("N8N_AI_INSTAGRAM_CAROUSEL"),
    "instagram_reel": env("N8N_VIDEO_WEBHOOK_URL"),
    "facebook_image": env("N8N_AI_FACEBOOK_IMAGE"),
    "facebook_video": env("N8N_AI_FACEBOOK_VIDEO"),
    "facebook_carousel": env("N8N_AI_FACEBOOK_CAROUSEL"),
    "twitter_post": env("N8N_AI_TWITTER_POST"),
    "linkedin_post": env("N8N_AI_LINKEDIN_POST"),
}

N8N_WEBHOOK_URL = os.environ.get("N8N_WEBHOOK_URL")
N8N_SECRET = os.environ.get("N8N_SECRET")
N8N_GEMINI_CALLBACK_SECRET = os.environ.get("N8N_GEMINI_SECRET")
N8N_META_WEBHOOK_URL = os.environ.get("N8N_META_WEBHOOK_URL")
N8N_PUBLISH_WEBHOOK_URL = os.environ.get("N8N_PUBLISH_WEBHOOK_URL")
N8N_POST_INSTAGRAM_WEBHOOK_URL = os.environ.get("N8N_POST_INSTAGRAM_WEBHOOK_URL")
N8N_INSTAGRAM_CAROUSELL_WEBHOOK_URL = os.environ.get("N8N_INSTAGRAM_CAROUSELL_WEBHOOK_URL")
N8N_VIDEO_WEBHOOK_URL = os.environ.get("N8N_VIDEO_WEBHOOK_URL")
N8N_EDIT_WEBHOOK_URL = os.environ.get("N8N_EDIT_WEBHOOK_URL")
N8N_CHATBOT_WEBHOOK_WHATSAPP = os.environ.get("N8N_CHATBOT_WEBHOOK_WHATSAPP")
WHATSAPP_BUSINESS_API = os.environ.get("WHATSAPP_BUSINESS_API")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_FROM = os.getenv("TWILIO_WHATSAPP_FROM")

# Configuración de AWS S3
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME")
AWS_S3_ENDPOINT_URL = os.environ.get("AWS_S3_ENDPOINT_URL")

AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "max-age=86400",
    "ACL": "public-read"
}

# Coloca esto ABSOLUTAMENTE AL FINAL de tu settings.py (después de todo lo demás)

AWS_LOCATION = os.environ.get("AWS_LOCATION", "qn041app")

STATIC_URL = f'{AWS_S3_ENDPOINT_URL}/{AWS_LOCATION}/static/'
MEDIA_URL = f'{AWS_S3_ENDPOINT_URL}/{AWS_LOCATION}/media/'

# Forzamos los storages a S3 de forma estricta (sin usar os.environ.get aquí)
STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

# Directorio temporal local que Django usa solo para procesar antes de subir a S3
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')