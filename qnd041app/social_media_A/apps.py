from django.apps import AppConfig


class SocialMediaAConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'social_media_A'

    def ready(self):
        import social_media_A.signals
