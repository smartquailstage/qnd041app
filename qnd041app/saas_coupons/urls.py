from django.urls import path
from . import views

app_name = 'saas_coupons'

urlpatterns = [
    path('apply/', views.coupon_apply, name='apply'),
    path('convenio/', views.create_coupon_request, name='solicitud')
]
