from django.urls import path
from .views import BusinessSystemProjectDetailView
from .views import NoticiaListView, NoticiaDetailView
from . import views

app_name = 'business_customer_projects'

urlpatterns = [
    path('projects/create/', views.create_project, name='create_project'),
    path('projects/<int:project_id>/processes/create/', views.create_process, name='processes'),
    path('projects/<int:project_id>/automation/create/', views.create_automation, name='automation'),
    path('projects/<int:project_id>/ai/create/', views.create_ai, name='ai'),
    path('processes/<int:process_id>/qa_test/create/', views.create_qa_test, name='create_qa_test'),
    path('projects/<int:project_id>/cloud_resource/create/', views.create_cloud_resource, name='create_cloud_resource'),

    path('projects/<int:pk>/', BusinessSystemProjectDetailView.as_view(), name='project_detail'),
    path('payment_orders/', views.PaymentOrderListView.as_view(), name='paymentorder_list'),
    path('payment_orders/<int:pk>/', views.PaymentOrderDetailView.as_view(), name='paymentorder_detail'),

    path('Noticias/', NoticiaListView.as_view(), name='lista'),
    path('Noticias/<int:pk>/', NoticiaDetailView.as_view(), name='detalle'),
]

