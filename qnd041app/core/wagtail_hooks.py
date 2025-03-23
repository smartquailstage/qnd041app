from django.templatetags.static import static
from wagtail.admin.menu import MenuItem,SubmenuMenuItem
#from wagtail_modeladmin.menus import SubMenu

from django.urls import reverse
from django.utils.html import  format_html
from wagtail import hooks 
from django.template.loader import render_to_string
from django.urls import path, reverse,include




from shop.admin import CategoryAdmin


@hooks.register('register_category_url')
def register_category_url():
    return [
        path('ecommerce/', index, name='ecommerce'),
    ]

@hooks.register("insert_global_admin_css",order=100)
def global_admin_css():
    return format_html('<link rel="stylesheet" href="{}">', static("css/custom.css"))




@hooks.register("insert_global_admin_css", order=100)
def global_admin_css():
    return format_html('<link rel="stylesheet" href="{}">', static("css/custom.css"))



@hooks.register('register_admin_menu_item')
def register_custom_menu_item():
    # Genera la URL correctamente con reverse
    url = reverse('wagtailadmin_home')
    
    # Crea un nuevo elemento de menú con la URL generada
    return MenuItem(
        'Dashboard',  # El nombre del elemento
        url,  # Utiliza la URL generada por reverse
        classnames='icon icon-tasks',  # Clases CSS para el ícono del menú, usa iconos de Wagtail
        order=100  # El orden en que se muestra el ítem (menor valor, más arriba)
    )



