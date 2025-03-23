from .models import Order
from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register


@register(Order)
class Order(TranslationOptions):
    fields = ('first_name','last_name','email','phone','created','updated','paid','braintree_id','coupon','arrival_date_time','departure_date_time','agree_term','total','discount')


