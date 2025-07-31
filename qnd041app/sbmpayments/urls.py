from django.urls import path
from . import views
from django.utils.translation import gettext_lazy as _


app_name = 'sbmpayments'

urlpatterns = [
    path(_('process/'), views.payment_process, name='process'),
    path(_('done_trans/<int:order_id>/'), views.transfer_confirmations, name='done_trans'),
    path(_('done/'), views.payment_done, name='done'),
    path(_('canceled/'), views.payment_canceled, name='canceled'),
    path('paypal/process/<int:order_id>/', views.paypal_process, name='paypal_process'),
    path('paypal/execute/<int:order_id>/', views.paypal_execute, name='paypal_execute'),
    path('paypal/cancel/', views.paypal_cancel, name='paypal_cancel'),
    path('paypal/done/<int:order_id>/', views.paypal_done, name='paypal_done'),
    path('amazon/pay/process/<int:order_id>/', views.amazon_pay_process, name='amazon_pay_process'),
    path('amazon/pay/execute/<int:order_id>/', views.amazon_pay_execute, name='amazon_pay_execute'),
    path('amazon/pay/done/<int:order_id>/', views.amazon_pay_done, name='amazon_pay_done'),
    path('amazon/pay/cancel/', views.amazon_pay_cancel, name='amazon_pay_cancel'),
]
