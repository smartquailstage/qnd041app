from django.urls import path
from .views import BusinessSystemProjectDetailView


app_name = 'business_customer_projects'

urlpatterns = [
    path('projects/<int:pk>/', BusinessSystemProjectDetailView.as_view(), name='project_detail'),
]
