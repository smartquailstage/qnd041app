from django.urls import path
from . import views

app_name = 'saas_shop'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    
    # 👈 COLOCAR LA RUTA FIJA ANTES DE LAS RUTAS DINÁMICAS
    path('ai-chat/', views.ai_assistant_chat_view, name='ai_chat_view'),
    
    path('<slug:category_slug>/', views.product_list, 
         name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', views.product_detail,
         name='product_detail'),
]