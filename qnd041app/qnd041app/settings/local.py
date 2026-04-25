from .base_local import *
from decouple import config, Csv





DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR / 'db.sqlite3'),
    }
}


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!




WAGTAIL_SITE_NAME = "SmartQuail IT Cloud Business" 

# SECURITY WARNING: don't run with debug turned on in production!

#DEBUG = str(os.environ.get('DEBUG')) == "1"
#ENV_ALLOWED_HOST = os.environ.get("ENV_ALLOWED_HOST")
ALLOWED_HOSTS = ['*']
#if ENV_ALLOWED_HOST:   
#     ALLOWED_HOSTS = [ ENV_ALLOWED_HOST ]



import os

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
    "instagram_reel": env("N8N_AI_INSTAGRAM_REEL"),

    "facebook_image": env("N8N_AI_FACEBOOK_IMAGE"),
    "facebook_video": env("N8N_AI_FACEBOOK_VIDEO"),
    "facebook_carousel": env("N8N_AI_FACEBOOK_CAROUSEL"),

    "twitter_post": env("N8N_AI_TWITTER_POST"),
    "linkedin_post": env("N8N_AI_LINKEDIN_POST"),
}


ALLOWED_HOSTS = ['*']

# Configuración de Celery
CELERY_BROKER_URL = 'amqp://localhost'  # URL de RabbitMQ
CELERY_RESULT_BACKEND = 'rpc://'  # O usa otro backend si lo prefieres
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'



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


#Static files DevMod



DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


