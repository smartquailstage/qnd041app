from django.apps import AppConfig

class smartbusinessanalyticsdemoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    # Debe ser el nombre completo del módulo Python
    name = 'smartbusinessanalytics_demo'
    verbose_name = 'SmartBusinessAnalytics® (EAP)'

    def ready(self):
        import smartbusinessanalytics_demo.signals
