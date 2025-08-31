from django.apps import AppConfig

class SqshopConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'SQShop'

    def ready(self):
        # Importar el módulo que contiene las traducciones para registrar los modelos
        import SQShop.translation