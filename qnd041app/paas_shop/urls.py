from django.urls import path
from . import views

app_name = 'paas_shop'

urlpatterns = [
    path('ai-chat/', views.ai_assistant_chat_view, name='ai_chat_view'),
    path('', views.product_list, name='product_list'),
    path('<slug:category_slug>/', views.product_list, 
         name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', views.product_detail,
         name='product_detail'),
]