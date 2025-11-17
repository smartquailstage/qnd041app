from django.urls import path
from . import views
from django.utils.translation import gettext_lazy as _


app_name = 'saas_orders'

urlpatterns = [
    path('accept-terms/', views.accept_terms, name='accept_terms'),
    path(_('create/'), views.order_create, name='order_create'),
    path('detalle/<int:order_id>/', views.order_detail, name='order_detail'),
    path('admin/order/<int:order_id>/', views.admin_order_detail, name='admin_order_detail'),
    path('admin/order/<int:order_id>/pdf/', views.admin_order_pdf, name='admin_order_pdf'),
    path('admin/order/<int:order_id>/ebook/', views.admin_ebook_pdf, name='admin_ebook_pdf'),

    path('admin/contract_ip/<int:order_id>/ip/', views.admin_contract_ip_pdf, name='admin_contract_ip_pdf'),
    path('admin/contract_dev/<int:order_id>/dev/', views.admin_contract_development_pdf, name='admin_contract_development_pdf'),
    path('admin/contratct_cloud/<int:order_id>/cloud/', views.admin_contract_cloud_pdf, name='admin_contract_cloud_pdf'),
]


