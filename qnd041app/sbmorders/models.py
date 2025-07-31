from django.db import models
from sbmshop.models import SBMProduct, Category
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import RegexValidator
from decimal import Decimal
import datetime


class Order(models.Model):
    PAYMENT_CHOICES = [
        ('card', 'Tarjeta de Crédito'),
        ('bank_transfer', 'Transferencia Bancaria'),
        ('paypal', 'PayPal'),
        ('amazon_pay', 'Amazon Pay'),
    ]

    product_name =  models.CharField(max_length=100,null=True)
    project_name =  models.CharField(max_length=100,null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    business_name = models.CharField(max_length=50,null=True)
    RUC = models.CharField(max_length=50,null=True)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    phone_regex = RegexValidator(
        regex=r'^\+?593?\d{9,15}$',
        message="El número de teléfono debe estar en formato internacional. Ejemplo: +593XXXXXXXXX."
    )
    phonenumber = PhoneNumberField(
        verbose_name="Teléfono",
        validators=[phone_regex],
        default='+593'  # Código de área de Ecuador como valor por defecto
    )
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100,null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    expire = models.DateTimeField(null=True)
    paid = models.BooleanField(default=False)
    braintree_id = models.CharField(max_length=150, blank=True)
    iva = models.PositiveSmallIntegerField(default=12,null=True)
    product_category = models.ForeignKey(Category,
                              related_name='product_category_items',
                              on_delete=models.CASCADE, null =True, blank=True,help_text='Número de usuarios en su Negocio')
    payment_method = models.CharField(max_length=500,choices=PAYMENT_CHOICES,null=True, blank = True)

    accept_terms_and_conditions = models.BooleanField(default=False, verbose_name="Acepta los términos y condiciones del contrato")


    

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
    category = models.ForeignKey(Category,
                              related_name='items',
                              on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(SBMProduct,
                                related_name='order_items',
                                on_delete=models.CASCADE)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity


class BankTransfer(models.Model):
    BANK_CHOICES = [
        ('banco_pichincha', 'Banco de Pichincha'),
        ('produbanco', 'Banco Produbanco'),
        ('banco_internacional', 'Banco Internacional'),
        ('banco_guayaquil', 'Banco de Guayaquil'),
        ('banco_bolivariano', 'Banco Bolivariano'),
        ('banco_del_achira', 'Banco del Austro'),
        ('banco_de_los_andes', 'Banco de los Andes'),
        ('banco_comercial', 'Banco Comercial'),
        ('banco_territorial', 'Banco Territorial'),
        ('banco_nacional_de_fomento', 'Banco Nacional de Fomento'),
        ('banco_pacifico', 'Banco Pacífico'),
        ('banco_procredit', 'Banco ProCredit'),
        ('banco_machala', 'Banco de Machala'),
        ('banco_de_la_produccion', 'Banco de la Producción'),
        ('banco_davivienda', 'Banco Davivienda Ecuador'),
        ('banco_de_guayaquil_vision', 'Banco de Guayaquil Visión'),
        ('banco_union', 'Banco Unión'),
        ('banco_solidario', 'Banco Solidario'),
        ('banco_mercantil', 'Banco Mercantil'),
        ('banco_rural', 'Banco Rural'),
        ('banco_suramericano', 'Banco Suramericano'),
    ]

    order = models.OneToOneField('Order', on_delete=models.CASCADE)
    bank = models.CharField(max_length=500, choices=BANK_CHOICES)
    bank_id = models.CharField(max_length=80, verbose_name='Bank Transaction ID', null=True, blank=True)
    transfer_date = models.DateField(auto_now=True)
   # invoice = models.FileField(upload_to='products/smartbusinessmedia/CUSTOMERSTRANSFERS/%Y/%m/%d', blank=True)
    paid = models.BooleanField(default=False, verbose_name="Estado de pago", null= True, blank=True)
    
    # Campo para aceptar los términos y condiciones
    accept_terms_and_conditions = models.BooleanField(default=False, verbose_name="Acepta los términos y condiciones del contrato")

    def __str__(self):
        return f'Transferencia bancaria para la orden {self.order.id}'
    


