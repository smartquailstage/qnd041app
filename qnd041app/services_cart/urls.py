from django.urls import path
from . import views

app_name = 'services_cart'

urlpatterns = [
    # ---- Carrito para PaymentOrder ----
    path(
        'add/payment-order/<int:order_id>/',
        views.cart_add_payment_order,
        name='cart_add_payment_order'
    ),
    path(
        'remove/payment-order/<int:order_id>/',
        views.cart_remove_payment_order,
        name='cart_remove_payment_order'
    ),

    # ---- Carrito general ----
    path('', views.cart_detail, name='cart_detail'),
]
