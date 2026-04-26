from wagtail import hooks
from .viewsets import SocialMediaGroup
from django.templatetags.static import static
from wagtail.admin.menu import MenuItem
from django.urls import reverse, path
from django.utils.html import format_html
from wagtail import hooks
from wagtail.models import Revision



from wagtail import hooks


from django.urls import reverse

from wagtail import hooks
from wagtail.admin.menu import MenuItem



@hooks.register("insert_global_admin_css", order=100)
def global_admin_css():
    return format_html('<link rel="stylesheet" href="{}">', static("css/custom.css"))


@hooks.register('register_admin_menu_item')
def register_custom_menu_item():
    return MenuItem(
        'Inicio',  # Texto visible
        reverse('wagtailadmin_home'),  # Ruta
        icon_name='home',
        order=100
    )


from wagtail import hooks
from django.templatetags.static import static
from django.utils.safestring import mark_safe


@hooks.register("insert_global_admin_css")
def custom_branding_logo():
    return mark_safe(f"""
        <style>
            /* 🔥 Logo sidebar + header */
            .wagtail-logo,
            .sidebar__inner .logo,
            .wagtail-sidebar__brand img {{
                content: url('{static("img/PRODUCT_LOGOS/CRM_logo.png")}');
                max-height: 40px;
                width: auto;
            }}

            /* 🔥 Login logo */
            .login-logo img {{
                content: url('{static("img/PRODUCT_LOGOS/CRM_logo.png")}');
                max-height: 60px;
            }}
        </style>
    """)




@hooks.register("register_admin_viewset")
def register_viewsets():
    return SocialMediaGroup()