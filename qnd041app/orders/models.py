from django.db import models
from shop.models import Product
from decimal import Decimal
from django.contrib import admin
from phone_field import PhoneField
from django.core.validators import MinValueValidator, \
                                   MaxValueValidator
from coupons.models import Coupon
from django.utils.translation import gettext_lazy as _


class Order(models.Model):
    first_name = models.CharField(_('First name'), max_length=50)
    last_name = models.CharField(_('Last name'), max_length=50)
    email = models.EmailField(_('E-mail'))
    phone = models.CharField(blank=True, help_text=_('Contact phone number'),max_length=16)
    #address = models.CharField(_('address'), max_length=250)
    #postal_code = models.CharField(_('postal code'), max_length=20)
    #city = models.CharField(_('city'), max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    braintree_id = models.CharField(max_length=150, blank=True)
    coupon = models.ForeignKey(Coupon,
                               related_name='orders',
                               null=True,
                               blank=True,
                               on_delete=models.SET_NULL)
    arrival_date_time = models.DateTimeField(_('Date & time for Arrival to CC-floreana'),null=True)
    departure_date_time = models.DateTimeField(_('Date & time for Departure to CC-floreana'),null=True)
    #start_arrival_time = models.DateTimeField(_('Time for Arrival to CC-floreana'),null=True)
    #end_departure_time = models.DateTimeField(_('Time for Arrival to CC-floreana'),null=True)
    #departure = models.DateTimeField(_('Date for departure from CC-floreana'),null=True)
    agree_term = models.BooleanField(_('I accept the terms and conditions of this services.'),default=False,null=False,blank=False)
    total =  models.DecimalField(max_digits=1000, decimal_places=2,null=True,blank=True)
    discount = models.IntegerField(default=0,
                                   validators=[MinValueValidator(0),
                                               MaxValueValidator(100)])

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Reserva Online'
        verbose_name_plural = 'Reservas Online'

    def __str__(self):
        return 'Reserve to {}'.format(self.first_name +' '+ self.last_name)

    @property
    @admin.display(
        ordering='last_name',
        description='Full name',
    )
    def full_name(self):
        return self.first_name + ' ' + self.last_name



    def get_total_cost(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        total_price = total_cost - total_cost * (self.discount / Decimal('100'))
        return  total_price

    def save(self):
        self.total = self.get_total_cost()
        super (Order, self).save()

 


class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                related_name='order_items',
                                on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity
