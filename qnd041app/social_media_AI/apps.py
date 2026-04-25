from django.apps import AppConfig


class SocialMediaAiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'social_media_AI'

    def ready(self):
        import social_media_AI.signals
