from .models import BusinessSystemProject
from saas_orders.models import SaaSOrder
from paas_orders.models import PaaSOrder
from iaas_orders.models import IaaSOrder


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







from business_customer_projects.models import BusinessSystemProject
from saas_orders.models import SaaSOrder
from paas_orders.models import PaaSOrder


def business_projects_context(request):

    if not request.user.is_authenticated:

        return {
            'saas_order': None,
            'paas_order': None,
            'can_create_project': False,
            'all_projects': [],
            'projects_in_progress': [],
        }

    # =====================================================
    # SaaS Orders activas
    # =====================================================

    active_saas_order = SaaSOrder.objects.filter(
        user=request.user,
        is_active=True,
        force_paid=True
    ).first()

    # =====================================================
    # PaaS Orders activas
    # =====================================================

    active_paas_order = PaaSOrder.objects.filter(
        user=request.user,
        is_active=True,
        force_paid=True
    ).first()

    # =====================================================
    # Ordenes SaaS en progreso
    # =====================================================

    saas_in_progress = SaaSOrder.objects.filter(
        user=request.user,
        is_active=True,
        is_progress=True
    ).exists()

    # =====================================================
    # Ordenes PaaS en progreso
    # =====================================================

    paas_in_progress = PaaSOrder.objects.filter(
        user=request.user,
        is_active=True,
        is_progress=True
    ).exists()

    # =====================================================
    # Verificar si existe alguna orden válida
    # =====================================================

    has_valid_order = (
        active_saas_order is not None or
        active_paas_order is not None
    )

    # =====================================================
    # Verificar si hay proyectos en progreso
    # =====================================================

    has_order_in_progress = (
        saas_in_progress or
        paas_in_progress
    )

    # =====================================================
    # Permitir crear proyecto
    # =====================================================

    can_create_project = (
        has_valid_order and
        not has_order_in_progress
    )

    # =====================================================
    # Proyectos del usuario
    # =====================================================

    user_projects = BusinessSystemProject.objects.filter(
        user=request.user
    )

    completed_projects = user_projects.filter(
        progress=100
    )

    in_progress_projects = user_projects.exclude(
        progress=100
    )

    return {
        'saas_order': active_saas_order,
        'paas_order': active_paas_order,
        'can_create_project': can_create_project,
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
