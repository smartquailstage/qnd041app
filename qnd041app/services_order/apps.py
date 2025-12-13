from django.apps import AppConfig


class SaaSOrdersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'services_orders'

    def ready(self):
        import services_orders.signals
