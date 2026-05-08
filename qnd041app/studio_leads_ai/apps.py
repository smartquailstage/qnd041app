from django.apps import AppConfig


class StudioLeadsAiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'studio_leads_ai'
    
    def ready(self):
        import studio_leads_ai.signals

