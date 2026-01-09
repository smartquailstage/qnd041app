from .models import BusinessSystemProject
from saas_orders.models import SaaSOrder


from usuarios.models import Profile

def tamano_empresa_context(request):
    """
    Procesador de contexto que expone el tamaño de la empresa
    SOLO del usuario autenticado.
    """
    tamano_empresa = None

    if request.user.is_authenticated:
        try:
            profile = Profile.objects.select_related('user').get(user=request.user)
            tamano_empresa = profile.tamano_empresa
        except Profile.DoesNotExist:
            tamano_empresa = None

    return {
        'tamano_empresa': tamano_empresa
    }



def business_projects_context(request):
    # Usuario no autenticado → no hay datos
    if not request.user.is_authenticated:
        return {
            'all_projects': [],
            'projects_in_progress': [],
        }

    # Verificar si el usuario tiene una orden activa
    has_active_order = SaaSOrder.objects.filter(
        user=request.user,
        is_active=True  # ajusta este campo si es distinto
    ).exists()

    # Si NO tiene orden activa → no exponer proyectos
    if not has_active_order:
        return {
            'all_projects': [],
            'projects_in_progress': [],
        }

    # Proyectos del usuario
    user_projects = BusinessSystemProject.objects.filter(user=request.user)

    # Proyectos completados
    completed_projects = user_projects.filter(progress=100)

    # Proyectos en progreso
    in_progress_projects = user_projects.exclude(progress=100)

    return {
        'all_projects': completed_projects,
        'projects_in_progress': in_progress_projects,
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



from .models import Noticia

def noticias_context(request):
    noticias = Noticia.objects.filter(activa=True).select_related(
        'categoria'
    )

    return {
        'noticias': noticias
    }