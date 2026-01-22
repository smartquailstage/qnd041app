from decimal import Decimal
from django.conf import settings
from paas_shop.models import Product
from paas_coupons.models import Coupon  # Asegúrate que este modelo exista y tenga atributo discount


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.PAAS_CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.PAAS_CART_SESSION_ID] = {}
        self.cart = cart

        self.coupon_id = self.session.get('coupon_id')
        self._coupon = None

    @property
    def coupon(self):
        if self._coupon is None and self.coupon_id:
            try:
                self._coupon = Coupon.objects.get(id=self.coupon_id)
            except Coupon.DoesNotExist:
                self._coupon = None
        return self._coupon

    @coupon.setter
    def coupon(self, value):
        self._coupon = value
        if value:
            self.coupon_id = value.id
        else:
            self.coupon_id = None

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        product_map = {str(product.id): product for product in products}

        for product_id, item in self.cart.items():
            price = Decimal(item['price'])
            quantity = item['quantity']
            total_price = price * quantity

            yield {
                'product': product_map.get(product_id),
                'price': price,
                'quantity': quantity,
                'total_price': total_price,
            }



    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def add(self, product, quantity=1, update_quantity=False):
        product_id = str(product.id)

        # Usar price_amount, que es Decimal
        price_decimal = product.price_amount

        if price_decimal is None:
            price_decimal = Decimal('0.00')

        price_str = str(price_decimal)

        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': price_str,
            }
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity

        self.save()

    def save(self):
        # Guardar coupon_id en sesión para evitar serializar objetos
        if self.coupon_id:
            self.session['coupon_id'] = self.coupon_id
        else:
            self.session.pop('coupon_id', None)

        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        if settings.PAAS_CART_SESSION_ID in self.session:
            del self.session[settings.PAAS_CART_SESSION_ID]
        self.session.pop('coupon_id', None)
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
