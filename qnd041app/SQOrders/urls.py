from django.urls import path
from .views import calculator_view, infra_calculator_view

app_name = 'sqorders'


urlpatterns = [
    path('infra-calculadora/', infra_calculator_view, name='infra_calculadora'),
    path('calculadora/', calculator_view, name='calculadora'),
]
