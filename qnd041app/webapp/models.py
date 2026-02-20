import datetime
from django.db import models
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.utils.functional import cached_property
from django.http import Http404
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    MultiFieldPanel,
)

from wagtail import blocks
# from streams import blocks
# from wagtail.core import blocks


from wagtail.models import Page, Orderable
from wagtail.snippets.models import register_snippet
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.fields import StreamField, RichTextField
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.search import index
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.images.models import Image
# Modelo para los campos del formulario de la página de inicio
#class ConsultasHome(AbstractFormField):
#    page = ParentalKey('Home', on_delete=models.CASCADE, related_name='form_fields')

#    class Meta:
#        app_label = "webapp"

from usuarios.forms import LoginForm  # importa tu formulario

from datetime import datetime, timezone
from django.utils.timezone import now

class ProximamentePage(Page):
    descripcion = RichTextField(blank=True, verbose_name="Descripción")
    imagen_destacada = models.ForeignKey(
        Image,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Imagen destacada"
    )
    fecha_lanzamiento = models.DateTimeField(
        verbose_name="Fecha y hora del lanzamiento"
    )
    enlace_redes = models.URLField(
        blank=True,
        null=True,
        verbose_name="Enlace a redes sociales o sitio temporal"
    )

    content_panels = Page.content_panels + [
        FieldPanel('descripcion'),
        FieldPanel('fecha_lanzamiento'),
        FieldPanel('enlace_redes'),
        FieldPanel('imagen_destacada'),
    ]

    template = "webapp/proximamente/proximamente.html"

    @property
    def countdown(self):
        now_time = now()

        if self.fecha_lanzamiento <= now_time:
            return {
                "expired": True,
                "days": 0,
                "hours": 0,
                "minutes": 0,
                "seconds": 0,
            }

        delta = self.fecha_lanzamiento - now_time
        total_seconds = int(delta.total_seconds())

        days = total_seconds // (24 * 3600)
        hours = (total_seconds % (24 * 3600)) // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60

        return {
            "expired": False,
            "days": days,
            "hours": hours,
            "minutes": minutes,
            "seconds": seconds,
        }


# Modelo para la página de inicio
class Home(Page):
    template = "webapp/home/home.html"

    # Campos de texto para banners
    banner_title4 = RichTextField(blank=True, verbose_name='Título de galería-1')
    TS_info1 = models.CharField(max_length=500, null=True, blank=True, verbose_name='Subtítulo info')
    info1 = models.CharField(max_length=500, null=True, blank=True, verbose_name='Info')

    banner_title5 = RichTextField(blank=True, verbose_name='Título de galería-2')
    TS_info2 = models.CharField(max_length=150, null=True, blank=True, verbose_name='Subtítulo-2 info')
    info2 = models.CharField(max_length=150, null=True, blank=True, verbose_name='Info-2')

    banner_title6 = RichTextField(blank=True, verbose_name='Título de galería-3')
    TS_info3 = models.CharField(max_length=150, null=True, blank=True, verbose_name='Subtítulo-3 info')
    info3 = models.CharField(max_length=150, null=True, blank=True, verbose_name='Info-3')

    banner_title7 = RichTextField(blank=True, verbose_name='Título de galería-4')
    TS_info4 = models.CharField(max_length=250, null=True, blank=True, verbose_name='Subtítulo-4 info')
    info4 = models.CharField(max_length=250, null=True, blank=True, verbose_name='Info-4')

    banner_title8 = RichTextField(blank=True, verbose_name='Título de galería-5')
    TS_info5 = models.CharField(max_length=250, null=True, blank=True, verbose_name='Subtítulo-5 info')
    info5 = models.CharField(max_length=250, null=True, blank=True, verbose_name='Info-5')

    banner_title9 = RichTextField(blank=True, verbose_name='Título de galería-6')
    TS_info6 = models.CharField(max_length=250, null=True, blank=True, verbose_name='Subtítulo-6 info')
    info6 = models.CharField(max_length=250, null=True, blank=True, verbose_name='Info-6')

    banner_title10 = RichTextField(blank=True, verbose_name='Título de galería-7')
    TS_info7 = models.CharField(max_length=250, null=True, blank=True, verbose_name='Subtítulo-7 info')
    info7 = models.CharField(max_length=250, null=True, blank=True, verbose_name='Info-7')

    # Callout
    banner_title10 = RichTextField(blank=True, verbose_name='Mejoramos')
    info7 = models.CharField(max_length=280, null=True, blank=True, verbose_name='IT Business Analytics')
    info8 = models.CharField(max_length=280, null=True, blank=True, verbose_name='IT Business Cloud DevOps')
    info9 = models.CharField(max_length=280, null=True, blank=True, verbose_name='IT Business Media')

    # Productos
    for i in range(1, 7):
        locals()[f'product_{i}'] = models.CharField(max_length=150, null=True, blank=True, verbose_name=f'Producto-{i}')
        locals()[f'product_description_{i}'] = models.CharField(max_length=150, null=True, blank=True, verbose_name=f'Descripción Producto-{i}')

    # Contadores
    numero_coffe =models.CharField(max_length=150, null=True, blank=True, verbose_name="Servicios IT Entregados")
    numero_experiencia = models.CharField(max_length=150, null=True, blank=True, verbose_name="Seguridad")
    numero_horas  = models.CharField(max_length=150, null=True, blank=True, verbose_name="Gobernanza IT")
    numero_wins= models.CharField(max_length=150, null=True, blank=True, verbose_name="Calidad de Servicio")

    # Equipo
    for i in range(1, 5):
        locals()[f'team_{i}'] = models.CharField(max_length=150, null=True, blank=True, verbose_name=f'Equipo-{i}')
        locals()[f'team_descrp_{i}'] = models.CharField(max_length=150, null=True, blank=True, verbose_name=f'Descripción Equipo-{i}')

    # Adicionales
    banner_title = models.CharField(max_length=150, null=True, blank=True, verbose_name='Título de llamada a la acción')
    slogan = models.CharField(max_length=150, null=True, blank=True, verbose_name='Slogan')
    slogan_descriptcion = models.CharField(max_length=150, null=True, blank=True, verbose_name='Descripción del Slogan')
    custom_title = models.CharField(max_length=100, blank=True, null=True, help_text="Reescribe el Título de la publicación")
    consulta = RichTextField(blank=True, verbose_name='Mensaje para consulta')
    thank_you_text = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        # Galerías
        FieldPanel("banner_title4"),
        FieldPanel("TS_info1"),
        FieldPanel("info1"),

        FieldPanel("banner_title5"),
        FieldPanel("TS_info2"),
        FieldPanel("info2"),

        FieldPanel("banner_title6"),
        FieldPanel("TS_info3"),
        FieldPanel("info3"),

        FieldPanel("banner_title7"),
        FieldPanel("TS_info4"),
        FieldPanel("info4"),

        FieldPanel("banner_title8"),
        FieldPanel("TS_info5"),
        FieldPanel("info5"),

        FieldPanel("banner_title9"),
        FieldPanel("TS_info6"),
        FieldPanel("info6"),

        FieldPanel("banner_title10"),
        FieldPanel("TS_info7"),
        FieldPanel("info7"),

        # Callout
        FieldPanel("banner_title10"),
        FieldPanel("info7"),
        FieldPanel("info8"),
        FieldPanel("info9"),

        # Productos
        FieldPanel("product_1"),
        FieldPanel("product_description_1"),
        FieldPanel("product_2"),
        FieldPanel("product_description_2"),
        FieldPanel("product_3"),
        FieldPanel("product_description_3"),
        FieldPanel("product_4"),
        FieldPanel("product_description_4"),
        FieldPanel("product_5"),
        FieldPanel("product_description_5"),
        FieldPanel("product_6"),
        FieldPanel("product_description_6"),

        # Contadores
        FieldPanel("numero_coffe"),
        FieldPanel("numero_experiencia"),
        FieldPanel("numero_horas"),
        FieldPanel("numero_wins"),

        # Equipo
        FieldPanel("team_1"),
        FieldPanel("team_descrp_1"),
        FieldPanel("team_2"),
        FieldPanel("team_descrp_2"),
        FieldPanel("team_3"),
        FieldPanel("team_descrp_3"),
        FieldPanel("team_4"),
        FieldPanel("team_descrp_4"),

        # Adicionales
        FieldPanel("banner_title"),
        FieldPanel("slogan"),
        FieldPanel("slogan_descriptcion"),
        FieldPanel("custom_title"),
        FieldPanel("consulta"),
        FieldPanel("thank_you_text"),

        InlinePanel('galleria', label="Imagenes de Fondo Barner"),
    ]





class GaleriaHome(Orderable):
    page = ParentalKey('Home', on_delete=models.CASCADE, related_name='galleria')

    logo = models.ForeignKey(
        Image, null=True, blank=True, on_delete=models.SET_NULL,
        related_name='+', verbose_name='Logotipo SmartQuail'
    )
    profile_pic = models.ForeignKey(
        Image, null=True, blank=True, on_delete=models.SET_NULL,
        related_name='+', verbose_name='Foto de perfil'
    )

    # Imagen principal
    image = models.ForeignKey(
        Image, null=True, blank=True, on_delete=models.SET_NULL,
        related_name='+', verbose_name='Imagen Slide Banner 1'
    )

    # Imagenes 2 al 26
    image_2 = models.ForeignKey(Image, null=True, blank=True, on_delete=models.SET_NULL, related_name='+', verbose_name='Imagen Slide Banner 2')
    image_3 = models.ForeignKey(Image, null=True, blank=True, on_delete=models.SET_NULL, related_name='+', verbose_name='Imagen Slide Banner 3')
    image_4 = models.ForeignKey(Image, null=True, blank=True, on_delete=models.SET_NULL, related_name='+', verbose_name='Imagen Slide Banner 4')
    image_5 = models.ForeignKey(Image, null=True, blank=True, on_delete=models.SET_NULL, related_name='+', verbose_name='Imagen Slide Banner 5')
    image_6 = models.ForeignKey(Image, null=True, blank=True, on_delete=models.SET_NULL, related_name='+', verbose_name='Imagen Slide Banner 6')
    image_7 = models.ForeignKey(Image, null=True, blank=True, on_delete=models.SET_NULL, related_name='+', verbose_name='Imagen Slide Banner 7')
    image_8 = models.ForeignKey(Image, null=True, blank=True, on_delete=models.SET_NULL, related_name='+', verbose_name='Imagen Slide Banner 8')
    image_9 = models.ForeignKey(Image, null=True, blank=True, on_delete=models.SET_NULL, related_name='+', verbose_name='Imagen Slide Banner 9')
    image_9_10 = models.ForeignKey(Image, null=True, blank=True, on_delete=models.SET_NULL, related_name='+', verbose_name='Imagen Slide Banner 100')
    image_10 = models.ForeignKey(Image, null=True, blank=True, on_delete=models.SET_NULL, related_name='+', verbose_name='Imagen Slide Banner 10')
    image_11 = models.ForeignKey(Image, null=True, blank=True, on_delete=models.SET_NULL, related_name='+', verbose_name='Imagen Slide Banner 11')
    image_12 = models.ForeignKey(Image, null=True, blank=True, on_delete=models.SET_NULL, related_name='+', verbose_name='Imagen Slide Banner 12')
    image_13 = models.ForeignKey(Image, null=True, blank=True, on_delete=models.SET_NULL, related_name='+', verbose_name='Imagen Slide Banner 13')
    image_14 = models.ForeignKey(Image, null=True, blank=True, on_delete=models.SET_NULL, related_name='+', verbose_name='Imagen Slide Banner 14')
    image_15 = models.ForeignKey(Image, null=True, blank=True, on_delete=models.SET_NULL, related_name='+', verbose_name='Imagen Slide Banner 15')
    image_16 = models.ForeignKey(Image, null=True, blank=True, on_delete=models.SET_NULL, related_name='+', verbose_name='Imagen Slide Banner 16')
    image_17 = models.ForeignKey(Image, null=True, blank=True, on_delete=models.SET_NULL, related_name='+', verbose_name='Imagen Slide Banner 17')
    image_18 = models.ForeignKey(Image, null=True, blank=True, on_delete=models.SET_NULL, related_name='+', verbose_name='Imagen Slide Banner 18')
    image_19 = models.ForeignKey(Image, null=True, blank=True, on_delete=models.SET_NULL, related_name='+', verbose_name='Imagen Slide Banner 19')
    image_20 = models.ForeignKey(Image, null=True, blank=True, on_delete=models.SET_NULL, related_name='+', verbose_name='Imagen Slide Banner 20')
    image_21 = models.ForeignKey(Image, null=True, blank=True, on_delete=models.SET_NULL, related_name='+', verbose_name='Imagen Slide Banner 21')
    image_22 = models.ForeignKey(Image, null=True, blank=True, on_delete=models.SET_NULL, related_name='+', verbose_name='Imagen Slide Banner 22')
    image_23 = models.ForeignKey(Image, null=True, blank=True, on_delete=models.SET_NULL, related_name='+', verbose_name='Imagen Slide Banner 23')
    image_24 = models.ForeignKey(Image, null=True, blank=True, on_delete=models.SET_NULL, related_name='+', verbose_name='Imagen Slide Banner 24')
    image_25 = models.ForeignKey(Image, null=True, blank=True, on_delete=models.SET_NULL, related_name='+', verbose_name='Imagen Slide Banner 25')
    image_26 = models.ForeignKey(Image, null=True, blank=True, on_delete=models.SET_NULL, related_name='+', verbose_name='Imagen Slide Banner 26')

    panels = [
        FieldPanel('logo'),
        FieldPanel('profile_pic'),
        FieldPanel('image'),
        FieldPanel('image_2'),
        FieldPanel('image_3'),
        FieldPanel('image_4'),
        FieldPanel('image_5'),
        FieldPanel('image_6'),
        FieldPanel('image_7'),
        FieldPanel('image_8'),
        FieldPanel('image_9'),
        FieldPanel('image_9_10'),
        FieldPanel('image_10'),
        FieldPanel('image_11'),
        FieldPanel('image_12'),
        FieldPanel('image_13'),
        FieldPanel('image_14'),
        FieldPanel('image_15'),
        FieldPanel('image_16'),
        FieldPanel('image_17'),
        FieldPanel('image_18'),
        FieldPanel('image_19'),
        FieldPanel('image_20'),
        FieldPanel('image_21'),
        FieldPanel('image_22'),
        FieldPanel('image_23'),
        FieldPanel('image_24'),
        FieldPanel('image_25'),
        FieldPanel('image_26'),
    ]



@register_setting
class SocialMediaSettings(BaseSiteSetting):
    facebook = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    youtube = models.URLField(blank=True, null=True)
    pinterest = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("facebook"),
                FieldPanel("twitter"),
                FieldPanel("instagram"),
                FieldPanel("youtube"),
                FieldPanel("pinterest"),
                FieldPanel("linkedin"),
            ],
            heading="Configuración de Redes Sociales"
        )
    ]

class info(Page):
    # Empieza Barner de Inicio
    template = "webapp/info/introduccion.html"
    #cliente_Navbar = RichTextField(blank=True,verbose_name='Cliente-url')
    
   # banner_title1 = RichTextField(blank=True,verbose_name='Titulo del primer banner ')
   # banner_info1 = RichTextField(blank=True,verbose_name='Informacion del primer banner ')
   # banner_title2 = RichTextField(blank=True,verbose_name='Titulo del segundo banner ')
   # banner_info2 = RichTextField(blank=True,verbose_name='Informacion del segundo banner ')
   # banner_title3 = RichTextField(blank=True,verbose_name='Titulo del tercer banner ')
   # banner_info3 = RichTextField(blank=True,verbose_name='Informacion del tercer banner ')

    # Empieza Banner de sliders
    bio2 = RichTextField(blank=True,verbose_name='Frase relevante primer parrafo')
    bio3 = RichTextField(blank=True,verbose_name='Frase relevante segundo parrafo')
    author_name = models.CharField(max_length=150, null=True, blank=True,verbose_name='Nombre de autor')
    business_title = models.CharField(max_length=150, null=True, blank=True,verbose_name='Titulo de autor en el negocio')
    business_activiy = models.CharField(max_length=150, null=True, blank=True,verbose_name='Actividad de autor en el negocio')
    business_experience = models.CharField(max_length=150, null=True, blank=True,verbose_name='años de experiencia de autor en el negocio')
    updated = models.CharField(max_length=150, null=True, blank=True,verbose_name='Fecha de ultima actualización')

    banner_title4 = RichTextField(blank=True,verbose_name='Titulo de galeria-1 ')
    TS_info1 = models.CharField(max_length=150, null=True, blank=True,verbose_name='project_info')
    TS_info2 = models.CharField(max_length=150, null=True, blank=True,verbose_name='project_info2')
    TS_info3 = models.CharField(max_length=150, null=True, blank=True,verbose_name='project2_info')
    info3 = models.CharField(max_length=150, null=True, blank=True,verbose_name='project2_info2')

    TS_info4 = models.CharField(max_length=150, null=True, blank=True,verbose_name='project3_info')
    info4 = models.CharField(max_length=150, null=True, blank=True,verbose_name='project3_info2')
    TS_info5 = models.CharField(max_length=150, null=True, blank=True,verbose_name='project4_info')
    info5 = models.CharField(max_length=150, null=True, blank=True,verbose_name='project4_info2')


    banner_title9 = RichTextField(blank=True,verbose_name='Titulo de parrafo')
    TS_info6 = models.CharField(max_length=350, null=True, blank=True,verbose_name='Subtitulo de parrafo')
    info_title9 = RichTextField(blank=True,verbose_name='Texto')

    banner_title10 = RichTextField(blank=True,verbose_name='Titulo de parrafo-2')
    TS_info7 = models.CharField(max_length=350, null=True, blank=True,verbose_name='Subtitulo de parrafo-2')
    info_title10 = RichTextField(blank=True,verbose_name='Texto-2')

    banner_title11 = RichTextField(blank=True,verbose_name='Titulo de parrafo-3')
    TS_info8 = models.CharField(max_length=350, null=True, blank=True,verbose_name='Subtitulo de parrafo-3')
    info_title11 = RichTextField(blank=True,verbose_name='Texto-3')
    info_title12 = RichTextField(blank=True,verbose_name='Descripcion de producto')

    banner_title13 = RichTextField(blank=True,verbose_name='Titulo de parrafo-3')
    info_title13 = RichTextField(blank=True,verbose_name='Descripcion de producto')
    banner_title14 = RichTextField(blank=True,verbose_name='Titulo de parrafo-3')
    info_title14 = RichTextField(blank=True,verbose_name='Descripcion de producto')

    banner_title15 = RichTextField(blank=True,verbose_name='Titulo de parrafo-3')
    info_title15 = RichTextField(blank=True,verbose_name='Descripcion de producto')


    link1 = RichTextField(blank=True,verbose_name='link-para empezar proyecto')
    link2 = RichTextField(blank=True,verbose_name='link-para contactos')

    banner_title12 = RichTextField(blank=True,verbose_name='invitacion a contactarnos')


    custom_title = models.CharField(max_length=100,blank=True,null=True,help_text="Reescribe el  Titulo de la publicacion ")


    
    # Campos de consulta

    consulta= RichTextField(blank=True,verbose_name='Mensaje para que nos consulten por el formulario')
    thank_you_text = RichTextField(blank=True)
    # galeria de imagenes barner de presentacion

    content_panels = Page.content_panels + [


    #Panel sliders
        FieldPanel('bio2', classname="full"),
        FieldPanel('bio3', classname="full"),

        FieldPanel('author_name', classname="full"),
        FieldPanel('business_title', classname="full"),
        FieldPanel('business_activiy', classname="full"),
        FieldPanel('business_experience', classname="full"),
        FieldPanel('updated', classname="full"),

        FieldPanel('banner_title4', classname="full"),
        FieldPanel('TS_info1', classname="full"),
        FieldPanel('TS_info2', classname="full"),
        FieldPanel('TS_info3', classname="full"),
        FieldPanel('info3', classname="full"),
        FieldPanel('TS_info4', classname="full"),
        FieldPanel('info4', classname="full"),
        FieldPanel('TS_info5', classname="full"),
        FieldPanel('info5', classname="full"),
        FieldPanel('banner_title9', classname="full"),
        FieldPanel('TS_info6', classname="full"),
        FieldPanel('info_title9', classname="full"),
        FieldPanel('banner_title10', classname="full"),
        FieldPanel('TS_info7', classname="full"),
        FieldPanel('info_title10', classname="full"),
        FieldPanel('banner_title11', classname="full"),
        FieldPanel('info_title11', classname="full"),
        FieldPanel('banner_title12', classname="full"),
        FieldPanel('info_title12', classname="full"),
        FieldPanel('banner_title13', classname="full"),
        FieldPanel('info_title13', classname="full"),
        FieldPanel('banner_title14', classname="full"),
        FieldPanel('info_title14', classname="full"),
        FieldPanel('banner_title15', classname="full"),
        FieldPanel('info_title15', classname="full"),
        FieldPanel('TS_info8', classname="full"),
        
        FieldPanel('link1', classname="full"),
        FieldPanel('link2', classname="full"),
   
#panel 
        FieldPanel('consulta', classname="full"),
        InlinePanel('galleria_3', label="Imagen de Fondo Barner"),
#Panel capo de noticas
        FieldPanel("custom_title"),
    ]

class GaleriadeImagenes(Orderable):
    page = ParentalKey(info, on_delete=models.CASCADE, related_name='galleria_3')
    banner_background = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Backgound en slide')
    logo_slide = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Logotipo en slide')
    logo = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Logotipo en texto ')
    profile_pic = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto de perfil')
    image = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 1')
    image_1 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 2')
    image_2_2 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 3')
    image_2 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 4')
    image_3_3 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 5')

    image_3 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 6')
    image_4_4 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 7')
    image_4 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 8')




    panels = [
        FieldPanel('banner_background'),
        FieldPanel('logo_slide'),
        FieldPanel('logo'),
        FieldPanel('profile_pic'),
        FieldPanel('image'),
        FieldPanel('image_2'),
        FieldPanel('image_3'),
        FieldPanel('image_4'),
        FieldPanel('image_1'),
        FieldPanel('image_2_2'),
        FieldPanel('image_3_3'),
        FieldPanel('image_4_4'),
    ]

@register_setting
class GlobalLinksSettings(BaseSiteSetting):
    contacus = models.URLField(blank=True,null=True,help_text="")
    start_project_SBM = models.URLField(blank=True,null=True,help_text="")
    start_project_SBL = models.URLField(blank=True,null=True,help_text="")
    start_project_SBA = models.URLField(blank=True,null=True,help_text="")
    start_project_SBT = models.URLField(blank=True,null=True,help_text="")


    panels = [
        MultiFieldPanel(
            [
            FieldPanel("contacus"),
            FieldPanel("start_project_SBM"),
            FieldPanel("start_project_SBL"),
            FieldPanel("start_project_SBA"),  
            FieldPanel("start_project_SBT"),         
            ]
        ,heading= "Global Links Settings")
    ]



class info_2(Page):
    # Empieza Barner de Inicio
    template = "webapp/info/mision_vision.html"
    #cliente_Navbar = RichTextField(blank=True,verbose_name='Cliente-url')
    
   # banner_title1 = RichTextField(blank=True,verbose_name='Titulo del primer banner ')
   # banner_info1 = RichTextField(blank=True,verbose_name='Informacion del primer banner ')
   # banner_title2 = RichTextField(blank=True,verbose_name='Titulo del segundo banner ')
   # banner_info2 = RichTextField(blank=True,verbose_name='Informacion del segundo banner ')
   # banner_title3 = RichTextField(blank=True,verbose_name='Titulo del tercer banner ')
   # banner_info3 = RichTextField(blank=True,verbose_name='Informacion del tercer banner ')

    # Empieza Banner de sliders
    bio2 = RichTextField(blank=True,verbose_name='Frase relevante primer parrafo')
    bio3 = RichTextField(blank=True,verbose_name='Frase relevante segundo parrafo')
    author_name = models.CharField(max_length=150, null=True, blank=True,verbose_name='Nombre de autor')
    business_title = models.CharField(max_length=150, null=True, blank=True,verbose_name='Titulo de autor en el negocio')
    business_activiy = models.CharField(max_length=150, null=True, blank=True,verbose_name='Actividad de autor en el negocio')
    business_experience = models.CharField(max_length=150, null=True, blank=True,verbose_name='años de experiencia de autor en el negocio')
    updated = models.CharField(max_length=150, null=True, blank=True,verbose_name='Fecha de ultima actualización')

    banner_title4 = RichTextField(blank=True,verbose_name='Titulo de galeria-1 ')
    TS_info1 = models.CharField(max_length=150, null=True, blank=True,verbose_name='project_info')
    TS_info2 = models.CharField(max_length=150, null=True, blank=True,verbose_name='project_info2')
    TS_info3 = models.CharField(max_length=150, null=True, blank=True,verbose_name='project2_info')
    info3 = models.CharField(max_length=150, null=True, blank=True,verbose_name='project2_info2')

    TS_info4 = models.CharField(max_length=150, null=True, blank=True,verbose_name='project3_info')
    info4 = models.CharField(max_length=150, null=True, blank=True,verbose_name='project3_info2')
    TS_info5 = models.CharField(max_length=150, null=True, blank=True,verbose_name='project4_info')
    info5 = models.CharField(max_length=150, null=True, blank=True,verbose_name='project4_info2')


    banner_title9 = RichTextField(blank=True,verbose_name='Titulo de parrafo')
    TS_info6 = models.CharField(max_length=350, null=True, blank=True,verbose_name='Subtitulo de parrafo')
    info_title9 = RichTextField(blank=True,verbose_name='Texto')

    banner_title10 = RichTextField(blank=True,verbose_name='Titulo de parrafo-2')
    TS_info7 = models.CharField(max_length=350, null=True, blank=True,verbose_name='Subtitulo de parrafo-2')
    info_title10 = RichTextField(blank=True,verbose_name='Texto-2')

    banner_title11 = RichTextField(blank=True,verbose_name='Titulo de parrafo-3')
    TS_info8 = models.CharField(max_length=350, null=True, blank=True,verbose_name='Subtitulo de parrafo-3')
    info_title11 = RichTextField(blank=True,verbose_name='Texto-3')
    info_title12 = RichTextField(blank=True,verbose_name='Descripcion de producto')

    banner_title13 = RichTextField(blank=True,verbose_name='Titulo de parrafo-3')
    info_title13 = RichTextField(blank=True,verbose_name='Descripcion de producto')
    banner_title14 = RichTextField(blank=True,verbose_name='Titulo de parrafo-3')
    info_title14 = RichTextField(blank=True,verbose_name='Descripcion de producto')

    banner_title15 = RichTextField(blank=True,verbose_name='Titulo de parrafo-3')
    info_title15 = RichTextField(blank=True,verbose_name='Descripcion de producto')


    link1 = RichTextField(blank=True,verbose_name='link-para empezar proyecto')
    link2 = RichTextField(blank=True,verbose_name='link-para contactos')

    banner_title12 = RichTextField(blank=True,verbose_name='invitacion a contactarnos')


    custom_title = models.CharField(max_length=100,blank=True,null=True,help_text="Reescribe el  Titulo de la publicacion ")


    
    # Campos de consulta

    consulta= RichTextField(blank=True,verbose_name='Mensaje para que nos consulten por el formulario')
    thank_you_text = RichTextField(blank=True)
    # galeria de imagenes barner de presentacion

    content_panels =  Page.content_panels + [


    #Panel sliders
        FieldPanel('bio2', classname="full"),
        FieldPanel('bio3', classname="full"),

        FieldPanel('author_name', classname="full"),
        FieldPanel('business_title', classname="full"),
        FieldPanel('business_activiy', classname="full"),
        FieldPanel('business_experience', classname="full"),
        FieldPanel('updated', classname="full"),

        FieldPanel('banner_title4', classname="full"),
        FieldPanel('TS_info1', classname="full"),
        FieldPanel('TS_info2', classname="full"),
        FieldPanel('TS_info3', classname="full"),
        FieldPanel('info3', classname="full"),
        FieldPanel('TS_info4', classname="full"),
        FieldPanel('info4', classname="full"),
        FieldPanel('TS_info5', classname="full"),
        FieldPanel('info5', classname="full"),
        FieldPanel('banner_title9', classname="full"),
        FieldPanel('TS_info6', classname="full"),
        FieldPanel('info_title9', classname="full"),
        FieldPanel('banner_title10', classname="full"),
        FieldPanel('TS_info7', classname="full"),
        FieldPanel('info_title10', classname="full"),
        FieldPanel('banner_title11', classname="full"),
        FieldPanel('info_title11', classname="full"),
        FieldPanel('banner_title12', classname="full"),
        FieldPanel('info_title12', classname="full"),
        FieldPanel('banner_title13', classname="full"),
        FieldPanel('info_title13', classname="full"),
        FieldPanel('banner_title14', classname="full"),
        FieldPanel('info_title14', classname="full"),
        FieldPanel('banner_title15', classname="full"),
        FieldPanel('info_title15', classname="full"),
        FieldPanel('TS_info8', classname="full"),
        
        FieldPanel('link1', classname="full"),
        FieldPanel('link2', classname="full"),
   
#panel 
        FieldPanel('consulta', classname="full"),
        InlinePanel('galleria_3_1', label="Imagen de Fondo Barner"),
#Panel capo de noticas
        FieldPanel("custom_title"),
    ]

class GaleriadeImagenesInfo2(Orderable):
    page = ParentalKey(info_2, on_delete=models.CASCADE, related_name='galleria_3_1')
    banner_background = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Backgound en slide')
    logo_slide = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Logotipo en slide')
    logo = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Logotipo en texto ')
    profile_pic = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto de perfil')
    image = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 1')
    image_1 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 1')
    image_2_2 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 1')
    image_2 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 2')
    image_3_3 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 1')

    image_3 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 3')
    image_4_4 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 1')
    image_4 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 4')


    panels = [
        FieldPanel('banner_background'),
        FieldPanel('logo_slide'),
        FieldPanel('logo'),
        FieldPanel('profile_pic'),
        FieldPanel('image'),
        FieldPanel('image_2'),
        FieldPanel('image_3'),
        FieldPanel('image_4'),
        FieldPanel('image_1'),
        FieldPanel('image_2_2'),
        FieldPanel('image_3_3'),
        FieldPanel('image_4_4'),
    ]

class smartbusinessmedia_info(Page):
    # Empieza Barner de Inicio
    template = "webapp/products/smartbusinessmedia/info/info.html"
    #cliente_Navbar = RichTextField(blank=True,verbose_name='Cliente-url')
    
   # banner_title1 = RichTextField(blank=True,verbose_name='Titulo del primer banner ')
   # banner_info1 = RichTextField(blank=True,verbose_name='Informacion del primer banner ')
   # banner_title2 = RichTextField(blank=True,verbose_name='Titulo del segundo banner ')
   # banner_info2 = RichTextField(blank=True,verbose_name='Informacion del segundo banner ')
   # banner_title3 = RichTextField(blank=True,verbose_name='Titulo del tercer banner ')
   # banner_info3 = RichTextField(blank=True,verbose_name='Informacion del tercer banner ')

    # Empieza Banner de sliders
    bio2 = RichTextField(blank=True,verbose_name='Frase relevante primer parrafo')
    bio3 = RichTextField(blank=True,verbose_name='Frase relevante segundo parrafo')
    author_name = models.CharField(max_length=150, null=True, blank=True,verbose_name='Nombre de autor')
    business_title = models.CharField(max_length=150, null=True, blank=True,verbose_name='Titulo de autor en el negocio')
    business_activiy = models.CharField(max_length=150, null=True, blank=True,verbose_name='Actividad de autor en el negocio')
    business_experience = models.CharField(max_length=150, null=True, blank=True,verbose_name='años de experiencia de autor en el negocio')
    updated = models.CharField(max_length=150, null=True, blank=True,verbose_name='Fecha de ultima actualización')

    banner_title4 = RichTextField(blank=True,verbose_name='Titulo de galeria-1 ')
    TS_info1 = models.CharField(max_length=150, null=True, blank=True,verbose_name='project_info')
    TS_info2 = models.CharField(max_length=150, null=True, blank=True,verbose_name='project_info2')
    TS_info3 = models.CharField(max_length=150, null=True, blank=True,verbose_name='project2_info')
    info3 = models.CharField(max_length=150, null=True, blank=True,verbose_name='project2_info2')

    TS_info4 = models.CharField(max_length=150, null=True, blank=True,verbose_name='project3_info')
    info4 = models.CharField(max_length=150, null=True, blank=True,verbose_name='project3_info2')
    TS_info5 = models.CharField(max_length=150, null=True, blank=True,verbose_name='project4_info')
    info5 = models.CharField(max_length=150, null=True, blank=True,verbose_name='project4_info2')


    banner_title9 = RichTextField(blank=True,verbose_name='Titulo de parrafo')
    TS_info6 = models.CharField(max_length=350, null=True, blank=True,verbose_name='Subtitulo de parrafo')
    info_title9 = RichTextField(blank=True,verbose_name='Texto')

    banner_title10 = RichTextField(blank=True,verbose_name='Titulo de parrafo-2')
    TS_info7 = models.CharField(max_length=350, null=True, blank=True,verbose_name='Subtitulo de parrafo-2')
    info_title10 = RichTextField(blank=True,verbose_name='Texto-2')

    banner_title11 = RichTextField(blank=True,verbose_name='Titulo de parrafo-3')
    TS_info8 = models.CharField(max_length=350, null=True, blank=True,verbose_name='Subtitulo de parrafo-3')
    info_title11 = RichTextField(blank=True,verbose_name='Texto-3')
    info_title12 = RichTextField(blank=True,verbose_name='Descripcion de producto')

    banner_title13 = RichTextField(blank=True,verbose_name='Titulo de parrafo-3')
    info_title13 = RichTextField(blank=True,verbose_name='Descripcion de producto')
    banner_title14 = RichTextField(blank=True,verbose_name='Titulo de parrafo-3')
    info_title14 = RichTextField(blank=True,verbose_name='Descripcion de producto')

    banner_title15 = RichTextField(blank=True,verbose_name='Titulo de parrafo-3')
    info_title15 = RichTextField(blank=True,verbose_name='Descripcion de producto')

    banner_title16 = RichTextField(blank=True,verbose_name='Titulo de parrafo-3')
    info_title16 = RichTextField(blank=True,verbose_name='Descripcion de producto')

    banner_title17 = RichTextField(blank=True,verbose_name='Titulo de parrafo-3')
    info_title17 = RichTextField(blank=True,verbose_name='Descripcion de producto')


    link1 = RichTextField(blank=True,verbose_name='link-para empezar proyecto')
    link2 = RichTextField(blank=True,verbose_name='link-para contactos')

    banner_title12 = RichTextField(blank=True,verbose_name='invitacion a contactarnos')


    custom_title = models.CharField(max_length=100,blank=True,null=True,help_text="Reescribe el  Titulo de la publicacion ")


    
    # Campos de consulta

    consulta= RichTextField(blank=True,verbose_name='Mensaje para que nos consulten por el formulario')
    thank_you_text = RichTextField(blank=True)
    # galeria de imagenes barner de presentacion

    content_panels = Page.content_panels + [


    #Panel sliders
        FieldPanel('bio2', classname="full"),
        FieldPanel('bio3', classname="full"),

        FieldPanel('author_name', classname="full"),
        FieldPanel('business_title', classname="full"),
        FieldPanel('business_activiy', classname="full"),
        FieldPanel('business_experience', classname="full"),
        FieldPanel('updated', classname="full"),

        FieldPanel('banner_title4', classname="full"),
        FieldPanel('TS_info1', classname="full"),
        FieldPanel('TS_info2', classname="full"),
        FieldPanel('TS_info3', classname="full"),
        FieldPanel('info3', classname="full"),
        FieldPanel('TS_info4', classname="full"),
        FieldPanel('info4', classname="full"),
        FieldPanel('TS_info5', classname="full"),
        FieldPanel('info5', classname="full"),
        FieldPanel('banner_title9', classname="full"),
        FieldPanel('TS_info6', classname="full"),
        FieldPanel('info_title9', classname="full"),
        FieldPanel('banner_title10', classname="full"),
        FieldPanel('TS_info7', classname="full"),
        FieldPanel('info_title10', classname="full"),
        FieldPanel('banner_title11', classname="full"),
        FieldPanel('info_title11', classname="full"),
        FieldPanel('banner_title12', classname="full"),
        FieldPanel('info_title12', classname="full"),
        FieldPanel('banner_title13', classname="full"),
        FieldPanel('info_title13', classname="full"),
        FieldPanel('banner_title14', classname="full"),
        FieldPanel('info_title14', classname="full"),
        FieldPanel('banner_title15', classname="full"),
        FieldPanel('info_title15', classname="full"),
        FieldPanel('banner_title16', classname="full"),
        FieldPanel('info_title16', classname="full"),
        FieldPanel('banner_title17', classname="full"),
        FieldPanel('info_title17', classname="full"),
        FieldPanel('TS_info8', classname="full"),
        
        FieldPanel('link1', classname="full"),
        FieldPanel('link2', classname="full"),
   
#panel 
        FieldPanel('consulta', classname="full"),
        InlinePanel('galleria_SBM', label="Imagen de Fondo Barner"),
#Panel capo de noticas
        FieldPanel("custom_title"),
    ]

class GaleriadeImagenesSBM(Orderable):
    page = ParentalKey(smartbusinessmedia_info, on_delete=models.CASCADE, related_name='galleria_SBM')
    banner_background = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Backgound en slide')
    logo_slide = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Logotipo en slide')
    logo = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Logotipo en texto ')
    profile_pic = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto de perfil')
    image = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 1')
    image_1 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 1')
    image_2_2 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 1')
    image_2 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 2')
    image_3_3 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 1')

    image_3 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 3')
    image_4_4 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 1')
    image_4 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 4')


    panels = [
        FieldPanel('banner_background'),
        FieldPanel('logo_slide'),
        FieldPanel('logo'),
        FieldPanel('profile_pic'),
        FieldPanel('image'),
        FieldPanel('image_2'),
        FieldPanel('image_3'),
        FieldPanel('image_4'),
        FieldPanel('image_1'),
        FieldPanel('image_2_2'),
        FieldPanel('image_3_3'),
        FieldPanel('image_4_4'),
    ]

@register_setting
class GlobalLinksSettingsSBM(BaseSiteSetting):
    contacus = models.URLField(blank=True,null=True,help_text="")
    start_project_SBM = models.URLField(blank=True,null=True,help_text="")
    start_project_SBL = models.URLField(blank=True,null=True,help_text="")
    start_project_SBA = models.URLField(blank=True,null=True,help_text="")
    start_project_SBT = models.URLField(blank=True,null=True,help_text="")


    panels = [
        MultiFieldPanel(
            [
            FieldPanel("contacus"),
            FieldPanel("start_project_SBM"),
            FieldPanel("start_project_SBL"),
            FieldPanel("start_project_SBA"),  
            FieldPanel("start_project_SBT"),         
            ]
        ,heading= "Global Links Settings")
    ]



class smartbusinessanalytics_info(Page):
    # Empieza Barner de Inicio
    template = "webapp/products/smartbusinessanalytics/info/info.html"
    #cliente_Navbar = RichTextField(blank=True,verbose_name='Cliente-url')
    
   # banner_title1 = RichTextField(blank=True,verbose_name='Titulo del primer banner ')
   # banner_info1 = RichTextField(blank=True,verbose_name='Informacion del primer banner ')
   # banner_title2 = RichTextField(blank=True,verbose_name='Titulo del segundo banner ')
   # banner_info2 = RichTextField(blank=True,verbose_name='Informacion del segundo banner ')
   # banner_title3 = RichTextField(blank=True,verbose_name='Titulo del tercer banner ')
   # banner_info3 = RichTextField(blank=True,verbose_name='Informacion del tercer banner ')

    # Empieza Banner de sliders
    bio2 = RichTextField(blank=True,verbose_name='Frase relevante primer parrafo')
    bio3 = RichTextField(blank=True,verbose_name='Frase relevante segundo parrafo')
    author_name = models.CharField(max_length=150, null=True, blank=True,verbose_name='Nombre de autor')
    business_title = models.CharField(max_length=150, null=True, blank=True,verbose_name='Titulo de autor en el negocio')
    business_activiy = models.CharField(max_length=150, null=True, blank=True,verbose_name='Actividad de autor en el negocio')
    business_experience = models.CharField(max_length=150, null=True, blank=True,verbose_name='años de experiencia de autor en el negocio')
    updated = models.CharField(max_length=150, null=True, blank=True,verbose_name='Fecha de ultima actualización')

    banner_title4 = RichTextField(blank=True,verbose_name='Titulo de galeria-1 ')
    TS_info1 = models.CharField(max_length=150, null=True, blank=True,verbose_name='project_info')
    TS_info2 = models.CharField(max_length=150, null=True, blank=True,verbose_name='project_info2')
    TS_info3 = models.CharField(max_length=150, null=True, blank=True,verbose_name='project2_info')
    info3 = models.CharField(max_length=150, null=True, blank=True,verbose_name='project2_info2')

    TS_info4 = models.CharField(max_length=150, null=True, blank=True,verbose_name='project3_info')
    info4 = models.CharField(max_length=150, null=True, blank=True,verbose_name='project3_info2')
    TS_info5 = models.CharField(max_length=150, null=True, blank=True,verbose_name='project4_info')
    info5 = models.CharField(max_length=150, null=True, blank=True,verbose_name='project4_info2')


    banner_title9 = RichTextField(blank=True,verbose_name='Titulo de parrafo')
    TS_info6 = models.CharField(max_length=350, null=True, blank=True,verbose_name='Subtitulo de parrafo')
    info_title9 = RichTextField(blank=True,verbose_name='Texto')

    banner_title10 = RichTextField(blank=True,verbose_name='Titulo de parrafo-2')
    TS_info7 = models.CharField(max_length=350, null=True, blank=True,verbose_name='Subtitulo de parrafo-2')
    info_title10 = RichTextField(blank=True,verbose_name='Texto-2')

    banner_title11 = RichTextField(blank=True,verbose_name='Titulo de parrafo-3')
    TS_info8 = models.CharField(max_length=350, null=True, blank=True,verbose_name='Subtitulo de parrafo-3')
    info_title11 = RichTextField(blank=True,verbose_name='Texto-3')
    info_title12 = RichTextField(blank=True,verbose_name='Descripcion de producto')

    banner_title13 = RichTextField(blank=True,verbose_name='Titulo de parrafo-3')
    info_title13 = RichTextField(blank=True,verbose_name='Descripcion de producto')
    banner_title14 = RichTextField(blank=True,verbose_name='Titulo de parrafo-3')
    info_title14 = RichTextField(blank=True,verbose_name='Descripcion de producto')

    banner_title15 = RichTextField(blank=True,verbose_name='Titulo de parrafo-3')
    info_title15 = RichTextField(blank=True,verbose_name='Descripcion de producto')


    link1 = RichTextField(blank=True,verbose_name='link-para empezar proyecto')
    link2 = RichTextField(blank=True,verbose_name='link-para contactos')

    banner_title12 = RichTextField(blank=True,verbose_name='invitacion a contactarnos')


    custom_title = models.CharField(max_length=100,blank=True,null=True,help_text="Reescribe el  Titulo de la publicacion ")


    
    # Campos de consulta

    consulta= RichTextField(blank=True,verbose_name='Mensaje para que nos consulten por el formulario')
    thank_you_text = RichTextField(blank=True)
    # galeria de imagenes barner de presentacion

    content_panels =  Page.content_panels + [


    #Panel sliders
        FieldPanel('bio2', classname="full"),
        FieldPanel('bio3', classname="full"),

        FieldPanel('author_name', classname="full"),
        FieldPanel('business_title', classname="full"),
        FieldPanel('business_activiy', classname="full"),
        FieldPanel('business_experience', classname="full"),
        FieldPanel('updated', classname="full"),

        FieldPanel('banner_title4', classname="full"),
        FieldPanel('TS_info1', classname="full"),
        FieldPanel('TS_info2', classname="full"),
        FieldPanel('TS_info3', classname="full"),
        FieldPanel('info3', classname="full"),
        FieldPanel('TS_info4', classname="full"),
        FieldPanel('info4', classname="full"),
        FieldPanel('TS_info5', classname="full"),
        FieldPanel('info5', classname="full"),
        FieldPanel('banner_title9', classname="full"),
        FieldPanel('TS_info6', classname="full"),
        FieldPanel('info_title9', classname="full"),
        FieldPanel('banner_title10', classname="full"),
        FieldPanel('TS_info7', classname="full"),
        FieldPanel('info_title10', classname="full"),
        FieldPanel('banner_title11', classname="full"),
        FieldPanel('info_title11', classname="full"),
        FieldPanel('banner_title12', classname="full"),
        FieldPanel('info_title12', classname="full"),
        FieldPanel('banner_title13', classname="full"),
        FieldPanel('info_title13', classname="full"),
        FieldPanel('banner_title14', classname="full"),
        FieldPanel('info_title14', classname="full"),
        FieldPanel('banner_title15', classname="full"),
        FieldPanel('info_title15', classname="full"),
        FieldPanel('TS_info8', classname="full"),
        
        FieldPanel('link1', classname="full"),
        FieldPanel('link2', classname="full"),
   
#panel 
        FieldPanel('consulta', classname="full"),
        InlinePanel('galleria_3', label="Imagen de Fondo Barner"),
#Panel capo de noticas
        FieldPanel("custom_title"),
    ]

class GaleriadeImagenesSBA(Orderable):
    page = ParentalKey(smartbusinessanalytics_info, on_delete=models.CASCADE, related_name='galleria_3')
    banner_background = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Backgound en slide')
    logo_slide = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Logotipo en slide')
    logo = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Logotipo en texto ')
    profile_pic = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto de perfil')
    image = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 1')
    image_1 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 1')
    image_2_2 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 1')
    image_2 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 2')
    image_3_3 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 1')

    image_3 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 3')
    image_4_4 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 1')
    image_4 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 4')


    panels = [
        FieldPanel('banner_background'),
        FieldPanel('logo_slide'),
        FieldPanel('logo'),
        FieldPanel('profile_pic'),
        FieldPanel('image'),
        FieldPanel('image_2'),
        FieldPanel('image_3'),
        FieldPanel('image_4'),
        FieldPanel('image_1'),
        FieldPanel('image_2_2'),
        FieldPanel('image_3_3'),
        FieldPanel('image_4_4'),
    ]

@register_setting
class GlobalLinksSettingsSBA(BaseSiteSetting):
    contacus = models.URLField(blank=True,null=True,help_text="")
    start_project_SBM = models.URLField(blank=True,null=True,help_text="")
    start_project_SBL = models.URLField(blank=True,null=True,help_text="")
    start_project_SBA = models.URLField(blank=True,null=True,help_text="")
    start_project_SBT = models.URLField(blank=True,null=True,help_text="")


    panels = [
        MultiFieldPanel(
            [
            FieldPanel("contacus"),
            FieldPanel("start_project_SBM"),
            FieldPanel("start_project_SBL"),
            FieldPanel("start_project_SBA"),  
            FieldPanel("start_project_SBT"),         
            ]
        ,heading= "Global Links Settings")
    ]



class smartbusinesslaw_info(Page):
    # Empieza Barner de Inicio
    template = "webapp/products/smartbusinesslaw/info/info.html"
    #cliente_Navbar = RichTextField(blank=True,verbose_name='Cliente-url')
    
   # banner_title1 = RichTextField(blank=True,verbose_name='Titulo del primer banner ')
   # banner_info1 = RichTextField(blank=True,verbose_name='Informacion del primer banner ')
   # banner_title2 = RichTextField(blank=True,verbose_name='Titulo del segundo banner ')
   # banner_info2 = RichTextField(blank=True,verbose_name='Informacion del segundo banner ')
   # banner_title3 = RichTextField(blank=True,verbose_name='Titulo del tercer banner ')
   # banner_info3 = RichTextField(blank=True,verbose_name='Informacion del tercer banner ')

    # Empieza Banner de sliders
    bio2 = RichTextField(blank=True,verbose_name='Frase relevante primer parrafo')
    bio3 = RichTextField(blank=True,verbose_name='Frase relevante segundo parrafo')
    author_name = models.CharField(max_length=150, null=True, blank=True,verbose_name='Nombre de autor')
    business_title = models.CharField(max_length=150, null=True, blank=True,verbose_name='Titulo de autor en el negocio')
    business_activiy = models.CharField(max_length=150, null=True, blank=True,verbose_name='Actividad de autor en el negocio')
    business_experience = models.CharField(max_length=150, null=True, blank=True,verbose_name='años de experiencia de autor en el negocio')
    updated = models.CharField(max_length=150, null=True, blank=True,verbose_name='Fecha de ultima actualización')

    banner_title4 = RichTextField(blank=True,verbose_name='Titulo de galeria-1 ')
    TS_info1 = models.CharField(max_length=150, null=True, blank=True,verbose_name='project_info')
    TS_info2 = models.CharField(max_length=150, null=True, blank=True,verbose_name='project_info2')
    TS_info3 = models.CharField(max_length=150, null=True, blank=True,verbose_name='project2_info')
    info3 = models.CharField(max_length=150, null=True, blank=True,verbose_name='project2_info2')

    TS_info4 = models.CharField(max_length=150, null=True, blank=True,verbose_name='project3_info')
    info4 = models.CharField(max_length=150, null=True, blank=True,verbose_name='project3_info2')
    TS_info5 = models.CharField(max_length=150, null=True, blank=True,verbose_name='project4_info')
    info5 = models.CharField(max_length=150, null=True, blank=True,verbose_name='project4_info2')


    banner_title9 = RichTextField(blank=True,verbose_name='Titulo de parrafo')
    TS_info6 = models.CharField(max_length=350, null=True, blank=True,verbose_name='Subtitulo de parrafo')
    info_title9 = RichTextField(blank=True,verbose_name='Texto')

    banner_title10 = RichTextField(blank=True,verbose_name='Titulo de parrafo-2')
    TS_info7 = models.CharField(max_length=350, null=True, blank=True,verbose_name='Subtitulo de parrafo-2')
    info_title10 = RichTextField(blank=True,verbose_name='Texto-2')

    banner_title11 = RichTextField(blank=True,verbose_name='Titulo de parrafo-3')
    TS_info8 = models.CharField(max_length=350, null=True, blank=True,verbose_name='Subtitulo de parrafo-3')
    info_title11 = RichTextField(blank=True,verbose_name='Texto-3')
    info_title12 = RichTextField(blank=True,verbose_name='Descripcion de producto')

    banner_title13 = RichTextField(blank=True,verbose_name='Titulo de parrafo-3')
    info_title13 = RichTextField(blank=True,verbose_name='Descripcion de producto')
    banner_title14 = RichTextField(blank=True,verbose_name='Titulo de parrafo-3')
    info_title14 = RichTextField(blank=True,verbose_name='Descripcion de producto')

    banner_title15 = RichTextField(blank=True,verbose_name='Titulo de parrafo-3')
    info_title15 = RichTextField(blank=True,verbose_name='Descripcion de producto')


    link1 = RichTextField(blank=True,verbose_name='link-para empezar proyecto')
    link2 = RichTextField(blank=True,verbose_name='link-para contactos')

    banner_title12 = RichTextField(blank=True,verbose_name='invitacion a contactarnos')


    custom_title = models.CharField(max_length=100,blank=True,null=True,help_text="Reescribe el  Titulo de la publicacion ")


    
    # Campos de consulta

    consulta= RichTextField(blank=True,verbose_name='Mensaje para que nos consulten por el formulario')
    thank_you_text = RichTextField(blank=True)
    # galeria de imagenes barner de presentacion

    content_panels = Page.content_panels + [


    #Panel sliders
        FieldPanel('bio2', classname="full"),
        FieldPanel('bio3', classname="full"),

        FieldPanel('author_name', classname="full"),
        FieldPanel('business_title', classname="full"),
        FieldPanel('business_activiy', classname="full"),
        FieldPanel('business_experience', classname="full"),
        FieldPanel('updated', classname="full"),

        FieldPanel('banner_title4', classname="full"),
        FieldPanel('TS_info1', classname="full"),
        FieldPanel('TS_info2', classname="full"),
        FieldPanel('TS_info3', classname="full"),
        FieldPanel('info3', classname="full"),
        FieldPanel('TS_info4', classname="full"),
        FieldPanel('info4', classname="full"),
        FieldPanel('TS_info5', classname="full"),
        FieldPanel('info5', classname="full"),
        FieldPanel('banner_title9', classname="full"),
        FieldPanel('TS_info6', classname="full"),
        FieldPanel('info_title9', classname="full"),
        FieldPanel('banner_title10', classname="full"),
        FieldPanel('TS_info7', classname="full"),
        FieldPanel('info_title10', classname="full"),
        FieldPanel('banner_title11', classname="full"),
        FieldPanel('info_title11', classname="full"),
        FieldPanel('banner_title12', classname="full"),
        FieldPanel('info_title12', classname="full"),
        FieldPanel('banner_title13', classname="full"),
        FieldPanel('info_title13', classname="full"),
        FieldPanel('banner_title14', classname="full"),
        FieldPanel('info_title14', classname="full"),
        FieldPanel('banner_title15', classname="full"),
        FieldPanel('info_title15', classname="full"),
        FieldPanel('TS_info8', classname="full"),
        
        FieldPanel('link1', classname="full"),
        FieldPanel('link2', classname="full"),
   
#panel 
        FieldPanel('consulta', classname="full"),
        InlinePanel('galleria_3', label="Imagen de Fondo Barner"),
#Panel capo de noticas
        FieldPanel("custom_title"),
    ]

class GaleriadeImagenesSBL(Orderable):
    page = ParentalKey(smartbusinesslaw_info, on_delete=models.CASCADE, related_name='galleria_3')
    banner_background = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Backgound en slide')
    logo_slide = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Logotipo en slide')
    logo = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Logotipo en texto ')
    profile_pic = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto de perfil')
    image = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 1')
    image_1 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 1')
    image_2_2 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 1')
    image_2 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 2')
    image_3_3 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 1')

    image_3 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 3')
    image_4_4 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 1')
    image_4 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 4')


    panels = [
        FieldPanel('banner_background'),
        FieldPanel('logo_slide'),
        FieldPanel('logo'),
        FieldPanel('profile_pic'),
        FieldPanel('image'),
        FieldPanel('image_2'),
        FieldPanel('image_3'),
        FieldPanel('image_4'),
        FieldPanel('image_1'),
        FieldPanel('image_2_2'),
        FieldPanel('image_3_3'),
        FieldPanel('image_4_4'),
    ]

@register_setting
class GlobalLinksSettingsSBL(BaseSiteSetting):
    contacus = models.URLField(blank=True,null=True,help_text="")
    start_project_SBM = models.URLField(blank=True,null=True,help_text="")
    start_project_SBL = models.URLField(blank=True,null=True,help_text="")
    start_project_SBA = models.URLField(blank=True,null=True,help_text="")
    start_project_SBT = models.URLField(blank=True,null=True,help_text="")


    panels = [
        MultiFieldPanel(
            [
            FieldPanel("contacus"),
            FieldPanel("start_project_SBM"),
            FieldPanel("start_project_SBL"),
            FieldPanel("start_project_SBA"),  
            FieldPanel("start_project_SBT"),         
            ]
        ,heading= "Global Links Settings")
    ]



class smartbusinesstechnologies_info(Page):
    # Empieza Barner de Inicio
    template = "webapp/products/smartbusinesstechnologies/info/info.html"
    #cliente_Navbar = RichTextField(blank=True,verbose_name='Cliente-url')
    
   # banner_title1 = RichTextField(blank=True,verbose_name='Titulo del primer banner ')
   # banner_info1 = RichTextField(blank=True,verbose_name='Informacion del primer banner ')
   # banner_title2 = RichTextField(blank=True,verbose_name='Titulo del segundo banner ')
   # banner_info2 = RichTextField(blank=True,verbose_name='Informacion del segundo banner ')
   # banner_title3 = RichTextField(blank=True,verbose_name='Titulo del tercer banner ')
   # banner_info3 = RichTextField(blank=True,verbose_name='Informacion del tercer banner ')

    # Empieza Banner de sliders
    bio2 = RichTextField(blank=True,verbose_name='Frase relevante primer parrafo')
    bio3 = RichTextField(blank=True,verbose_name='Frase relevante segundo parrafo')
    author_name = models.CharField(max_length=150, null=True, blank=True,verbose_name='Nombre de autor')
    business_title = models.CharField(max_length=150, null=True, blank=True,verbose_name='Titulo de autor en el negocio')
    business_activiy = models.CharField(max_length=150, null=True, blank=True,verbose_name='Actividad de autor en el negocio')
    business_experience = models.CharField(max_length=150, null=True, blank=True,verbose_name='años de experiencia de autor en el negocio')
    updated = models.CharField(max_length=150, null=True, blank=True,verbose_name='Fecha de ultima actualización')

    banner_title4 = RichTextField(blank=True,verbose_name='Titulo de galeria-1 ')
    TS_info1 = models.CharField(max_length=150, null=True, blank=True,verbose_name='project_info')
    TS_info2 = models.CharField(max_length=150, null=True, blank=True,verbose_name='project_info2')
    TS_info3 = models.CharField(max_length=150, null=True, blank=True,verbose_name='project2_info')
    info3 = models.CharField(max_length=150, null=True, blank=True,verbose_name='project2_info2')

    TS_info4 = models.CharField(max_length=150, null=True, blank=True,verbose_name='project3_info')
    info4 = models.CharField(max_length=150, null=True, blank=True,verbose_name='project3_info2')
    TS_info5 = models.CharField(max_length=150, null=True, blank=True,verbose_name='project4_info')
    info5 = models.CharField(max_length=150, null=True, blank=True,verbose_name='project4_info2')


    banner_title9 = RichTextField(blank=True,verbose_name='Titulo de parrafo')
    TS_info6 = models.CharField(max_length=350, null=True, blank=True,verbose_name='Subtitulo de parrafo')
    info_title9 = RichTextField(blank=True,verbose_name='Texto')

    banner_title10 = RichTextField(blank=True,verbose_name='Titulo de parrafo-2')
    TS_info7 = models.CharField(max_length=350, null=True, blank=True,verbose_name='Subtitulo de parrafo-2')
    info_title10 = RichTextField(blank=True,verbose_name='Texto-2')

    banner_title11 = RichTextField(blank=True,verbose_name='Titulo de parrafo-3')
    TS_info8 = models.CharField(max_length=350, null=True, blank=True,verbose_name='Subtitulo de parrafo-3')
    info_title11 = RichTextField(blank=True,verbose_name='Texto-3')
    info_title12 = RichTextField(blank=True,verbose_name='Descripcion de producto')

    banner_title13 = RichTextField(blank=True,verbose_name='Titulo de parrafo-3')
    info_title13 = RichTextField(blank=True,verbose_name='Descripcion de producto')
    banner_title14 = RichTextField(blank=True,verbose_name='Titulo de parrafo-3')
    info_title14 = RichTextField(blank=True,verbose_name='Descripcion de producto')

    banner_title15 = RichTextField(blank=True,verbose_name='Titulo de parrafo-3')
    info_title15 = RichTextField(blank=True,verbose_name='Descripcion de producto')


    link1 = RichTextField(blank=True,verbose_name='link-para empezar proyecto')
    link2 = RichTextField(blank=True,verbose_name='link-para contactos')

    banner_title12 = RichTextField(blank=True,verbose_name='invitacion a contactarnos')


    custom_title = models.CharField(max_length=100,blank=True,null=True,help_text="Reescribe el  Titulo de la publicacion ")


    
    # Campos de consulta

    consulta= RichTextField(blank=True,verbose_name='Mensaje para que nos consulten por el formulario')
    thank_you_text = RichTextField(blank=True)
    # galeria de imagenes barner de presentacion

    content_panels = Page.content_panels + [


    #Panel sliders
        FieldPanel('bio2', classname="full"),
        FieldPanel('bio3', classname="full"),

        FieldPanel('author_name', classname="full"),
        FieldPanel('business_title', classname="full"),
        FieldPanel('business_activiy', classname="full"),
        FieldPanel('business_experience', classname="full"),
        FieldPanel('updated', classname="full"),

        FieldPanel('banner_title4', classname="full"),
        FieldPanel('TS_info1', classname="full"),
        FieldPanel('TS_info2', classname="full"),
        FieldPanel('TS_info3', classname="full"),
        FieldPanel('info3', classname="full"),
        FieldPanel('TS_info4', classname="full"),
        FieldPanel('info4', classname="full"),
        FieldPanel('TS_info5', classname="full"),
        FieldPanel('info5', classname="full"),
        FieldPanel('banner_title9', classname="full"),
        FieldPanel('TS_info6', classname="full"),
        FieldPanel('info_title9', classname="full"),
        FieldPanel('banner_title10', classname="full"),
        FieldPanel('TS_info7', classname="full"),
        FieldPanel('info_title10', classname="full"),
        FieldPanel('banner_title11', classname="full"),
        FieldPanel('info_title11', classname="full"),
        FieldPanel('banner_title12', classname="full"),
        FieldPanel('info_title12', classname="full"),
        FieldPanel('banner_title13', classname="full"),
        FieldPanel('info_title13', classname="full"),
        FieldPanel('banner_title14', classname="full"),
        FieldPanel('info_title14', classname="full"),
        FieldPanel('banner_title15', classname="full"),
        FieldPanel('info_title15', classname="full"),
        FieldPanel('TS_info8', classname="full"),
        
        FieldPanel('link1', classname="full"),
        FieldPanel('link2', classname="full"),
   
#panel 
        FieldPanel('consulta', classname="full"),
        InlinePanel('galleria_3', label="Imagen de Fondo Barner"),
#Panel capo de noticas
        FieldPanel("custom_title"),
    ]

class GaleriadeImagenesSBT(Orderable):
    page = ParentalKey(smartbusinesstechnologies_info, on_delete=models.CASCADE, related_name='galleria_3')
    banner_background = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Backgound en slide')
    logo_slide = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Logotipo en slide')
    logo = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Logotipo en texto ')
    profile_pic = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto de perfil')
    image = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 1')
    image_1 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 1')
    image_2_2 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 1')
    image_2 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 2')
    image_3_3 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 1')

    image_3 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 3')
    image_4_4 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 1')
    image_4 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 4')


    panels = [
        FieldPanel('banner_background'),
        FieldPanel('logo_slide'),
        FieldPanel('logo'),
        FieldPanel('profile_pic'),
        FieldPanel('image'),
        FieldPanel('image_2'),
        FieldPanel('image_3'),
        FieldPanel('image_4'),
        FieldPanel('image_1'),
        FieldPanel('image_2_2'),
        FieldPanel('image_3_3'),
        FieldPanel('image_4_4'),
    ]

@register_setting
class GlobalLinksSettingsSBT(BaseSiteSetting):
    contacus = models.URLField(blank=True,null=True,help_text="")
    start_project_SBM = models.URLField(blank=True,null=True,help_text="")
    start_project_SBL = models.URLField(blank=True,null=True,help_text="")
    start_project_SBA = models.URLField(blank=True,null=True,help_text="")
    start_project_SBT = models.URLField(blank=True,null=True,help_text="")


    panels = [
        MultiFieldPanel(
            [
            FieldPanel("contacus"),
            FieldPanel("start_project_SBM"),
            FieldPanel("start_project_SBL"),
            FieldPanel("start_project_SBA"),  
            FieldPanel("start_project_SBT"),         
            ]
        ,heading= "Global Links Settings")
    ]



    import json
from os.path import splitext

from django.db import models
from django.core.serializers.json import DjangoJSONEncoder

from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
    FieldRowPanel,
)
from wagtail.contrib.forms.models import (
    AbstractEmailForm,
    AbstractFormField,
    FORM_FIELD_CHOICES,
)
from wagtail.contrib.forms.forms import FormBuilder
from wagtail.contrib.forms.panels import FormSubmissionsPanel
from wagtail.models import Collection

from wagtail.images import get_image_model
from wagtail.images.blocks import ImageChooserBlock
from wagtail import blocks

from modelcluster.fields import ParentalKey


# ------------------------------------------------------------------
# CHOICES
# ------------------------------------------------------------------

JOBS = (
    ("Marketing & Publishing", "Marketing & Publishing"),
    ("UI/UX Developer", "UI/UX Developer"),
    ("Python/Django Developer", "Python/Django Developer"),
    ("Docker Developer", "Docker Developer"),
    ("Kubernetes Developer", "Kubernetes Developer"),
    ("FullStack Developer", "FullStack Developer"),
    ("Chief Technology Officer", "Chief Technology Officer"),
    ("Chief Officer", "Chief Officer"),
)

JOBS_CATEGORY = (
    ("Community Manager Senior", "Community Manager Senior"),
    ("Community Manager Junior", "Community Manager Junior"),
    ("Content Designer Senior", "Content Designer Senior"),
    ("Content Designer Junior", "Content Designer Junior"),
    ("Project Manager Senior", "Project Manager Senior"),
    ("Project Manager Junior", "Project Manager Junior"),
    ("UI/UX Designer Senior", "UI/UX Designer Senior"),
    ("UI/UX Designer Junior", "UI/UX Designer Junior"),
    ("Django Developer Senior", "Django Developer Senior"),
    ("Django Developer Junior", "Django Developer Junior"),
    ("Site Reliability Engineer Senior", "Site Reliability Engineer Senior"),
    ("Site Reliability Engineer Junior", "Site Reliability Engineer Junior"),
)

CITIES = (
    ("Quito", "Quito"),
    ("Guayaquil", "Guayaquil"),
    ("Cuenca", "Cuenca"),
    ("Buenos Aires", "Buenos Aires"),
    ("Mendoza", "Mendoza"),
    ("Paris", "Paris"),
    ("Lausanne", "Lausanne"),
    ("New York", "New York"),
)

COUNTRIES = (
    ("Ecuador", "Ecuador"),
    ("Switzerland", "Switzerland"),
    ("Argentina", "Argentina"),
    ("France", "France"),
    ("United States", "United States"),
)

TIMEJOBS = (
    ("Part Time", "Part Time"),
    ("Full Time", "Full Time"),
)


# ------------------------------------------------------------------
# JOB LISTING PAGE
# ------------------------------------------------------------------

class JobsListingOpeningPage(Page):
    template = "webapp/joblistingopening.html"

    custom_title = models.CharField(
        max_length=100,
        help_text="Overwrites the default title",
    )

    jobs_category = models.CharField(
        max_length=100,
        choices=JOBS,
        blank=True,
        null=True,
    )

    benefits = RichTextField(
        blank=True,
        verbose_name="Beneficios"
    )

    content_panels = Page.content_panels + [
        FieldPanel("custom_title"),
        FieldPanel("jobs_category"),
        FieldPanel("benefits"),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context["posts"] = JobsFormDetailOpeningPage.objects.live().public()
        return context


# ------------------------------------------------------------------
# FORM FIELD (CUSTOM IMAGE FIELD)
# ------------------------------------------------------------------





from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, FieldRowPanel, InlinePanel
from wagtail.models import Page, Orderable, ParentalKey
from wagtail.fields import RichTextField
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField

# -------------------
# About Us Items
# -------------------


class aboutusPage(Page):
    template = "webapp/aboutus.html"

    custom_title = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        help_text='Overwrites the default title',
    )

    aboutus = RichTextField(blank=True, verbose_name='SmartQuail Story')

    content_panels = Page.content_panels + [
        FieldPanel("custom_title"),
        FieldPanel("aboutus"),
        InlinePanel('aboutus_items', label="Teams"),
    ]

class AboutUsPageItem(Orderable):
    page = ParentalKey(
        'aboutusPage',
        on_delete=models.CASCADE,
        related_name='aboutus_items'
    )

    image_1 = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Banner'
    )

    image_2 = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Profile Picture 1'
    )

    image_3 = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Profile Picture 2'
    )

    image_4 = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Profile Picture 3'
    )

    image_5 = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Profile Picture 4'
    )

    image_6 = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Profile Picture 5'
    )

    image_7 = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Profile Picture 6'
    )

    team1_name = models.CharField(max_length=100)
    team2_name = models.CharField(max_length=100)
    team3_name = models.CharField(max_length=100)
    team4_name = models.CharField(max_length=100)

    team1_position = models.CharField(max_length=100)
    team2_position = models.CharField(max_length=100)
    team3_position = models.CharField(max_length=100)
    team4_position = models.CharField(max_length=100)

    panels = [
        FieldPanel('image_1'),
        FieldPanel('image_2'),
        FieldPanel('image_3'),
        FieldPanel('image_4'),
        FieldPanel('image_5'),
        FieldPanel('image_6'),
        FieldPanel('image_7'),
        FieldPanel('team1_name'),
        FieldPanel('team2_name'),
        FieldPanel('team3_name'),
        FieldPanel('team4_name'),
        FieldPanel('team1_position'),
        FieldPanel('team2_position'),
        FieldPanel('team3_position'),
        FieldPanel('team4_position'),
    ]

# -------------------
# Portfolio Choices
# -------------------

PORTFOLIO = (
    ("Landscapes", "Landscapes"),
    ("Visual Production", "Visual Production"),
    ("Web Content", "Web Content"),
    ("Social Networks Content", "Social Networks Content"),
    ("Web Design", "Web Design"),
    ("Artificial Intelligence", "Artificial Intelligence"),
)

# -------------------
# Resume Form Fields
# -------------------

