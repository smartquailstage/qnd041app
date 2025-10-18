from django.apps import AppConfig


class BusinessCustomerProjectsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'business_customer_projects'

    def ready(self):
        import business_customer_projects.signals  # ✅ Nombre correcto del módulo
