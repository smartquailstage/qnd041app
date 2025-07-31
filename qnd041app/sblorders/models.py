from django.db import models
from sblshop.models import SBLProduct
from decimal import Decimal
import datetime


class Order(models.Model):
    product_name =  models.CharField(max_length=100,null=True)
    project_name =  models.CharField(max_length=100,null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    business_name = models.CharField(max_length=50,null=True)
    RUC = models.CharField(max_length=50,null=True)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100,null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    expire = models.DateTimeField(null=True)
    paid = models.BooleanField(default=False)
    braintree_id = models.CharField(max_length=150, blank=True)
    iva = models.PositiveSmallIntegerField(default=12,null=True)


    

    class Meta:
        ordering = ('-created',)


    def __str__(self):
        return 'Order {}'.format(self.id)
    

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())
    
    def Tax_calc(self):
        return self.iva / Decimal('100')
    
    def tax_subtotal(self):
        tax_subtotal_cost = (self.get_total_cost()*self.Tax_calc())
        return tax_subtotal_cost

    
    
    def total(self):
        tax_subtotal_cost = (self.get_total_cost()*self.Tax_calc()) + self.get_total_cost()
        return tax_subtotal_cost


class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE)
    product = models.ForeignKey(SBLProduct,
                                related_name='order_items',
                                on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity
    


