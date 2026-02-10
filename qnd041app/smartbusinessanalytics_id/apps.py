from django.apps import AppConfig

class SmartbusinessanalyticsIdConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    # Debe ser el nombre completo del módulo Python
    name = 'smartbusinessanalytics_id'
    verbose_name = 'SmartBusinessAnalytics® (I+D)'

    def ready(self):
        import smartbusinessanalytics_id.signals
