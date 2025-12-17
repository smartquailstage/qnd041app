from decimal import Decimal
from django.conf import settings
from business_customer_projects.models import PaymentOrder
from services_coupons.models import Coupon


class Cart:
    def __init__(self, request):
        self.session = request.session

        cart = self.session.get(settings.SERVICES_CART_SESSION_ID)
        if cart is None:
            cart = {}
            self.session[settings.SERVICES_CART_SESSION_ID] = cart

        self.cart = cart
        self.coupon_id = self.session.get('coupon_id')
        self._coupon = None

    # -------------------------
    # CUPÓN
    # -------------------------
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
        self.coupon_id = value.id if value else None
        self.save()

    # -------------------------
    # ITERADOR
    # -------------------------
    def __iter__(self):
        order_ids = self.cart.keys()
        orders = PaymentOrder.objects.filter(id__in=order_ids)
        order_map = {str(order.id): order for order in orders}

        for order_id, item in self.cart.items():
            order = order_map.get(order_id)
            if not order:
                continue

            price = Decimal(item['price'])
            quantity = item['quantity']

            yield {
                'payment_order': order,
                'price': price,
                'quantity': quantity,
                'total_price': price * quantity,
            }

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    # -------------------------
    # CRUD
    # -------------------------
    def add(self, payment_order, quantity=1, update_quantity=False):
        order_id = str(payment_order.id)
        price_decimal = payment_order.cost or Decimal('0.00')

        if order_id not in self.cart:
            self.cart[order_id] = {
                'quantity': 0,
                'price': str(price_decimal),
            }

        if update_quantity:
            self.cart[order_id]['quantity'] = quantity
        else:
            self.cart[order_id]['quantity'] += quantity

        self.save()

    def remove(self, payment_order):
        order_id = str(payment_order.id)
        if order_id in self.cart:
            del self.cart[order_id]
            self.save()

    def clear(self):
        self.cart = {}
        self.session[settings.SERVICES_CART_SESSION_ID] = {}
        self.session.pop('coupon_id', None)
        self.session.modified = True

    # -------------------------
    # TOTALES
    # -------------------------
    def save(self):
        self.session[settings.SERVICES_CART_SESSION_ID] = self.cart

        if self.coupon_id:
            self.session['coupon_id'] = self.coupon_id
        else:
            self.session.pop('coupon_id', None)

        self.session.modified = True

    def get_total_price(self):
        return sum(
            Decimal(item['price']) * item['quantity']
            for item in self.cart.values()
        )

    def get_discount(self):
        if self.coupon:
            return (self.coupon.discount / Decimal('100')) * self.get_total_price()
        return Decimal('0.00')

    def get_total_price_after_discount(self):
        return self.get_total_price() - self.get_discount()
