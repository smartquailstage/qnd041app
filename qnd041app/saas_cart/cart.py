import re
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
                price_str = item.get('price', '0.00')
                currency = item.get('currency', 'USD')

                # Extraer solo números, comas o puntos
                match = re.search(r'[\d.,]+', str(price_str))
                if match:
                    normalized_price_str = match.group().replace(',', '.')
                else:
                    normalized_price_str = '0.00'

                price = Decimal(normalized_price_str)
                item['price'] = Money(price, currency)
            except (InvalidOperation, TypeError, ValueError) as e:
                print(f"[ERROR] Precio inválido en carrito: {price_str} ({e})")
                item['price'] = Money(Decimal('0.00'), 'USD')

            try:
                item['total_price'] = item['price'] * item['quantity']
            except Exception as e:
                print(f"[ERROR] total_price error: {e}")
                item['total_price'] = Money(Decimal('0.00'), item['price'].currency)

            item['update_quantity_form'] = CartAddProductForm(initial={
                'quantity': item['quantity'],
                'update': True
            })

            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def add(self, product, quantity=1, update_quantity=False):
        product_id = str(product.id)

        # Validamos y convertimos correctamente el precio
        try:
            if isinstance(product.price, Money):
                price_money = product.price
            else:
                # Si es un número o string, intentamos convertir
                price_money = Money(Decimal(str(product.price)).quantize(Decimal('0.01')), 'USD')
        except Exception as e:
            print(f"[ERROR] product.price no válido para el producto {product_id}: {product.price} ({e})")
            price_money = Money(Decimal('0.00'), 'USD')

        amount = price_money.amount
        currency = price_money.currency.code

        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                # Guardar sólo la parte numérica como string, con punto decimal
                'price': f"{amount:.2f}",
                'currency': currency,
            }

        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity

        print(f"[DEBUG] Producto agregado al carrito: {product_id}, cantidad: {self.cart[product_id]['quantity']}, precio: {amount} {currency}")
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
            try:
                total += item['price'] * item['quantity']
            except Exception as e:
                print(f"[ERROR] get_total_price error: {e}")
        return total

    def get_discount(self):
        total_price = self.get_total_price()
        if self.coupon:
            try:
                discount_amount = total_price.amount * (self.coupon.discount / Decimal('100'))
                return Money(discount_amount, total_price.currency)
            except Exception as e:
                print(f"[ERROR] Error calculando descuento: {e}")
        return Money(Decimal('0.00'), 'USD')

    def get_total_price_after_discount(self):
        return self.get_total_price() - self.get_discount()
