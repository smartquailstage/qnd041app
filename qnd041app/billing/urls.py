# urls.py

from django.urls import path
from .views import FacturationListView, FacturationDetailView


app_name = 'billing'

urlpatterns = [
    path('facturas/', FacturationListView.as_view(), name='facturation_list'),
    path('facturas/<int:pk>/', FacturationDetailView.as_view(), name='facturation_detail'),
]
