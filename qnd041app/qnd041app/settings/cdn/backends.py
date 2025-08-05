from storages.backends.s3boto3 import S3Boto3Storage
import os

aws_location = os.environ.get("AWS_LOCATION", "qn041app")


class StaticRootS3BotoStorage(S3Boto3Storage):
    location = f"{aws_location}/static"
    default_acl = 'public-read'  
    file_overwrite = False

class MediaRootS3BotoStorage(S3Boto3Storage):
    location = f"{aws_location}/media"
    default_acl = 'public-read'  # ✅ Cambia a 'private' si quieres proteger los archivos multimedia
    file_overwrite = False



