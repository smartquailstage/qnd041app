from django.urls import path
from . import views

app_name = 'sbmorders'

urlpatterns = [
    path('sbmcreate/', views.order_create, name='order_create'),
    path('es/Sbmorders/bank_transfer/<int:order_id>/', views.bank_transfer_process, name='bank_transfer_process'),
    path('bank_transfer/<int:order_id>/', views.bank_transfer_process, name='bank_transfer_process'),
    path('amazon_pay/<int:order_id>/', views.amazon_pay_process, name='amazon_pay_process'),
    path('apple_pay/<int:order_id>/', views.apple_pay_process, name='apple_pay_process'),
    path('admin/order/<int:order_id>/', views.admin_order_detail, name='admin_order_detail'),
    path('admin/order/<int:order_id>/pdf/', views.admin_order_pdf, name='admin_order_pdf'),
]
