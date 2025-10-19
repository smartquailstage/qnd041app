from .models import Facturation
from business_customer_projects.models import BusinessSystemProject



def all_business_billing(request):
    if not request.user.is_authenticated:
        return {}

    user_projects = request.user.businesssystemproject_set.all()

    user_invoices = Facturation.objects.filter(project__in=user_projects)

    return {
        "has_facturation": user_invoices.exists(),
        "user_invoices": user_invoices,
    }