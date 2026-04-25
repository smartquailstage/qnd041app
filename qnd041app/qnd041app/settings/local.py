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


N8N_WEBHOOKS_A = {
    "instagram_post": "https://tu-n8n.com/webhook/instagram-post",
    "instagram_carousel": "https://tu-n8n.com/webhook/instagram-carousel",
    "instagram_reel": "https://tu-n8n.com/webhook/instagram-reel",

    "facebook_image": "https://tu-n8n.com/webhook/facebook-image",
    "facebook_video": "https://tu-n8n.com/webhook/facebook-video",
    "facebook_carousel": "https://tu-n8n.com/webhook/facebook-carousel",

    "twitter_post": "https://tu-n8n.com/webhook/twitter-post",
    "linkedin_post": "https://tu-n8n.com/webhook/linkedin-post",
}


N8N_WEBHOOKS_A_AI = {
    "instagram_post": "https://tu-n8n.com/webhook/instagram-post",
    "instagram_carousel": "https://tu-n8n.com/webhook/instagram-carousel",
    "instagram_reel": "https://tu-n8n.com/webhook/instagram-reel",

    "facebook_image": "https://tu-n8n.com/webhook/facebook-image",
    "facebook_video": "https://tu-n8n.com/webhook/facebook-video",
    "facebook_carousel": "https://tu-n8n.com/webhook/facebook-carousel",

    "twitter_post": "https://tu-n8n.com/webhook/twitter-post",
    "linkedin_post": "https://tu-n8n.com/webhook/linkedin-post",
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


