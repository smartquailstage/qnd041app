from django.apps import AppConfig


class PaaSOrdersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'paas_orders'

    def ready(self):
        import paas_orders.signals
