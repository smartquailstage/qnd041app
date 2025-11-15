from django.apps import AppConfig


class SaaSOrdersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'saas_orders'

    def ready(self):
        import saas_orders.signals
