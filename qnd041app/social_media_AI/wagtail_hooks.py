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





@hooks.register("register_admin_viewset")
def register_viewsets():
    return SocialMediaGroup()