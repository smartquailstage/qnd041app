from decimal import Decimal, InvalidOperation
from django.conf import settings
from djmoney.money import Money
from saas_shop.models import Product
from saas_coupons.models import Coupon
from .forms import CartAddProductForm


class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.SAAS_CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.SAAS_CART_SESSION_ID] = {}
        self.cart = cart

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
            try:
                price = item.get('price')
                currency = item.get('currency', 'USD')

                # Aseguramos que `price` sea un Decimal válido
                if not isinstance(price, Decimal):
                    price = Decimal(str(price))  # en caso esté como string

                # Convertimos a objeto Money
                item['price'] = Money(price, currency)

            except (InvalidOperation, TypeError, ValueError) as e:
                print(f"[ERROR] Invalid price in cart: {e}")
                item['price'] = Money(Decimal('0.00'), 'USD')  # Fallback

            item['total_price'] = item['price'] * item['quantity']

            item['update_quantity_form'] = CartAddProductForm(initial={
                'quantity': item['quantity'],
                'update': True
            })

            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def add(self, product, quantity=1, update_quantity=False):
        product_id = str(product.id)

        # Aseguramos obtener un Money válido con valor y moneda
        price_money = product.price or Money(Decimal('0.00'), 'USD')
        amount = price_money.amount if price_money.amount is not None else Decimal('0.00')
        currency = price_money.currency.code if price_money.currency else 'USD'

        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(amount),  # Guardamos como string porque el session no soporta Decimal/Money directamente
                'currency': currency,
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
        if settings.SAAS_CART_SESSION_ID in self.session:
            del self.session[settings.SAAS_CART_SESSION_ID]
        self.session.pop('coupon_id', None)
        self.save()

    def get_total_price(self):
        total = Money(Decimal('0.00'), 'USD')
        for item in self:
            total += item['price'] * item['quantity']
        return total

    def get_discount(self):
        total_price = self.get_total_price()
        if self.coupon:
            discount_amount = total_price.amount * (self.coupon.discount / Decimal('100'))
            return Money(discount_amount, total_price.currency)
        return Money(Decimal('0.00'), 'USD')

    def get_total_price_after_discount(self):
        return self.get_total_price() - self.get_discount()
