from .models import BusinessSystemProject

def business_projects_context(request):
    # Si no está autenticado, devolver vacío
    if not request.user.is_authenticated:
        return {
            'all_projects': [],
            'projects_in_progress': [],
        }

    # Todos los proyectos del usuario
    user_projects = BusinessSystemProject.objects.filter(user=request.user)

    # Completados
    completed_projects = user_projects.filter(progress=100)

    # En progreso
    in_progress = user_projects.exclude(progress=100)

    return {
        'all_projects': completed_projects,
        'projects_in_progress': in_progress,
    }



from django.db.models import Sum
from .models import PaymentOrder

from django.db.models import Sum, F, DecimalField, ExpressionWrapper
from .models import PaymentOrder


def pending_payment_orders_total(request):
    """
    Retorna el total acumulado (incluido IVA) de las órdenes de pago pendientes
    del usuario autenticado.
    """
    if not request.user.is_authenticated:
        return {
            "pending_orders_total": 0,
            "pending_orders_count": 0,
        }

    pending_orders = PaymentOrder.objects.filter(
        user=request.user,
        pago_verificado=False
    )

    total = pending_orders.aggregate(
        total=Sum(
            ExpressionWrapper(
                F('cost') + F('iva'),
                output_field=DecimalField(max_digits=12, decimal_places=2)
            )
        )
    )['total'] or 0

    return {
        "pending_orders_total": total,
        "pending_orders_count": pending_orders.count(),
    }

