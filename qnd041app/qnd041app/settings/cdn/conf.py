import os

# Configuración de AWS
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME")
AWS_S3_ENDPOINT_URL = os.environ.get("AWS_S3_ENDPOINT_URL").rstrip('/')
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "max-age=86400", 
    "ACL": "public-read"  # Cambia a 'private' si los archivos deben ser privados
}

# Configuración de almacenamiento
AWS_LOCATION = os.environ.get("AWS_LOCATION")  # 'static' o 'media'

# Asegúrate de que la URL de los archivos estáticos esté correcta
STATIC_URL = f'{AWS_S3_ENDPOINT_URL}/{AWS_LOCATION}/static'

# Almacenamiento de archivos estáticos
STATICFILES_STORAGE = os.environ.get("STATICFILES_STORAGE")

# Almacenamiento de archivos de medios
DEFAULT_FILE_STORAGE = os.environ.get("MEDIA_STORAGE")
MEDIA_URL = f"{AWS_S3_ENDPOINT_URL}/{AWS_LOCATION}/media/"

# Si usas DigitalOcean, añade esta configuración
AWS_S3_SIGNATURE_VERSION = 's3v4'
