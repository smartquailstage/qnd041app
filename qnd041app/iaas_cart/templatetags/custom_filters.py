# saas_cart/templatetags/custom_filters.py

from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    """Multiplica un valor por un argumento"""
    try:
        return value * float(arg)
    except (ValueError, TypeError):
        return value  # Devuelve el valor original si hay un error
