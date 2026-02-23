from django.templatetags.static import static
from wagtail.admin.menu import MenuItem
from django.urls import reverse, path
from django.utils.html import format_html
from wagtail import hooks
from wagtail.models import Revision
from .models import SocialAutomationPost
from .tasks import send_post_to_n8n




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





@hooks.register("after_publish_page")
def trigger_social_automation(request, page):
    """
    Hook que se dispara cuando una página se publica.
    Lanza la tarea de Celery para enviar el post a n8n.
    """
    if isinstance(page, SocialAutomationPost):
        if page.status == "pending":
            send_post_to_n8n.delay(page.id)