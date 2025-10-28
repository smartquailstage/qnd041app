from django.urls import path
from . import views

app_name = 'sbpshop'

urlpatterns = [
    path('smartbusinessproducts/', views.product_list, name='product_list'),
    path('<slug:category_slug>/', views.product_list, 
         name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', views.product_detail,
         name='product_detail'),
    path('admin/product/<int:manual_id>/pdf/', views.admin_product_manual_pdf, name='admin_product_manual_pdf'),
     
]