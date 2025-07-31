from django.urls import path
from . import views

app_name = 'sbmcoupons'

urlpatterns = [
    path('apply/', views.coupon_apply, name='apply'),
]
