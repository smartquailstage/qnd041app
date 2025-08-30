from django.urls import path
from . import views
from django.utils.translation import gettext_lazy as _


app_name = 'SQOrders'

urlpatterns = [
    path(_('create/'), views.order_create, name='order_create'),
    path(_('Order_terms/'), views.order_term, name='order_term'),
    path('admin/order/<int:order_id>/', views.admin_order_detail, name='admin_order_detail'),
    path('admin/order/<int:order_id>/phone', views.admin_order_phone, name='admin_order_phone'),
    path('admin/order/<int:order_id>/pdf/', views.admin_order_pdf, name='admin_order_pdf'),
]
