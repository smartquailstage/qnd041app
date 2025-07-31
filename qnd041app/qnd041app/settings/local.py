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





ALLOWED_HOSTS = ['*']

# Configuración de Celery
CELERY_BROKER_URL = 'amqp://localhost'  # URL de RabbitMQ
CELERY_RESULT_BACKEND = 'rpc://'  # O usa otro backend si lo prefieres
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'


#Static files DevMod



DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


