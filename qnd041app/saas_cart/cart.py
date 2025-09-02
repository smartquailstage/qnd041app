from decimal import Decimal
from django.conf import settings
from saas_shop.models import Product
from saas_coupons.models import Coupon  # Asegúrate de que este modelo existe


class Cart(object):

    def __init__(self, request):
        """
        Initialize the cart.
        """
        self.session = request.session
        cart = self.session.get(settings.SAAS_CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.SAAS_CART_SESSION_ID] = {}
        self.cart = cart

        # cupón (si está en sesión)
        self.coupon_id = self.session.get('coupon_id')
        self.coupon = None
        if self.coupon_id:
            try:
                self.coupon = Coupon.objects.get(id=self.coupon_id)
            except Coupon.DoesNotExist:
                self.coupon = None

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def add(self, product, quantity=1, update_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price)
            }
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        del self.session[settings.SAAS_CART_SESSION_ID]
        self.session.pop('coupon_id', None)  # limpia el cupón también
        self.save()

    def get_total_price(self):
        return sum(
            Decimal(item['price']) * item['quantity']
            for item in self.cart.values()
        )

    def get_discount(self):
        if self.coupon:
            return (self.coupon.discount / Decimal('100')) * self.get_total_price()
        return Decimal('0')

    def get_total_price_after_discount(self):
        return self.get_total_price() - self.get_discount()
