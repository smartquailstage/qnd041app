from storages.backends.s3boto3 import S3Boto3Storage

class StaticRootS3BotoStorage(S3Boto3Storage):
    location = "static"
    default_acl = 'public-read'  # ✅ Asegura que los archivos estáticos sean accesibles públicamente

class MediaRootS3BotoStorage(S3Boto3Storage):
    location = "media"
    default_acl = 'public-read'  # ✅ Cambia a 'private' si quieres proteger los archivos multimedia
