from django.templatetags.static import static
from wagtail.admin.menu import MenuItem
from django.urls import reverse, path
from django.utils.html import format_html
from wagtail import hooks


@hooks.register('register_category_url')
def register_category_url():
    return [
        path('ecommerce/', index, name='ecommerce'),
    ]


@hooks.register("insert_global_admin_css", order=100)
def global_admin_css():
    return format_html('<link rel="stylesheet" href="{}">', static("css/custom.css"))


@hooks.register('register_admin_menu_item')
def register_custom_menu_item():
    return MenuItem(
        'Dashboard',  # Texto visible
        reverse('wagtailadmin_home'),  # Ruta
        classname='icon icon-tasks',  # ✅ CORREGIDO: era classnames
        order=100
    )
