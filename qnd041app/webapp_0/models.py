import datetime
from django.db import models
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.utils.functional import cached_property
from django.http import Http404
from modelcluster.fields import ParentalKey
from modelcluster.tags import ClusterTaggableManager
from taggit.models import Tag as TaggitTag
from taggit.models import TaggedItemBase
from wagtail.admin.panels import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    MultiFieldPanel,
)
from streams import blocks
#from wagtail.core import blocks
from wagtail.models import Page,Orderable
from wagtail.snippets.models import register_snippet
from wagtail.fields import StreamField, RichTextField
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.search import index
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField



from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail import blocks




    



# pagina de inicio
class consultas(AbstractFormField):
    page = ParentalKey('index', on_delete=models.CASCADE, related_name='form_fields')

class Index(AbstractEmailForm):
    # Empieza Barner de Inicio
    template = "webapp_0/index.html"
    #cliente_Navbar = RichTextField(blank=True,verbose_name='Cliente-url')
    
   # banner_title1 = RichTextField(blank=True,verbose_name='Titulo del primer banner ')
   # banner_info1 = RichTextField(blank=True,verbose_name='Informacion del primer banner ')
   # banner_title2 = RichTextField(blank=True,verbose_name='Titulo del segundo banner ')
   # banner_info2 = RichTextField(blank=True,verbose_name='Informacion del segundo banner ')
   # banner_title3 = RichTextField(blank=True,verbose_name='Titulo del tercer banner ')
   # banner_info3 = RichTextField(blank=True,verbose_name='Informacion del tercer banner ')

    # Empieza Banner de Galerias
    bio = RichTextField(blank=True,verbose_name='rseña bibliografica')

    banner_title4 = RichTextField(blank=True,verbose_name='Titulo de galeria-1 ')
    banner_title5 = RichTextField(blank=True,verbose_name='Titulo de galeria-2  ')
    banner_title6 = RichTextField(blank=True,verbose_name='Titulo de galeria-3  ')
    banner_title7 = RichTextField(blank=True,verbose_name='Titulo de galeria-4  ')

    # Empieza Banner de Tearsheet
    TS_info1 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Tearsheet-1 info')
    TS_date1 = models.DateField("Fecha de Tearsheet-1",null=True, blank=True)
    TS_info2 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Tearsheet-2 info')
    TS_date2 = models.DateField("Fecha de Tearsheet-2",null=True, blank=True)
    TS_info3 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Tearsheet-3 info')
    TS_date3 = models.DateField("Fecha de Tearsheet-3",null=True, blank=True)
    TS_info4 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Tearsheet-4 info')
    TS_date4 = models.DateField("Fecha de Tearsheet-4",null=True, blank=True)
    TS_info5 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Tearsheet-5 info')
    TS_date5 = models.DateField("Fecha de Tearsheet-5",null=True, blank=True)
    TS_info6 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Tearsheet-6 info')
    TS_date6 = models.DateField("Fecha de Tearsheet-6",null=True, blank=True)
    TS_info7 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Tearsheet-7 info')
    TS_date7 = models.DateField("Fecha de Tearsheet-7",null=True, blank=True)
    TS_info8 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Tearsheet-8 info')
    TS_date8 = models.DateField("Fecha de Tearsheet-8",null=True, blank=True)
    TS_info9 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Tearsheet-9 info')
    TS_date9 = models.DateField("Fecha de Tearsheet-9",null=True, blank=True)
    TS_info10 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Tearsheet-10 info')
    TS_date10 = models.DateField("Fecha de Tearsheet-10",null=True, blank=True)
    TS_info11 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Tearsheet-11 info')
    TS_date11 = models.DateField("Fecha de Tearsheet-11",null=True, blank=True)
    TS_info12 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Tearsheet-12 info')
    TS_date12 = models.DateField("Fecha de Tearsheet-12",null=True, blank=True)
    TS_info13 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Tearsheet-13 info')
    TS_date13 = models.DateField("Fecha de Tearsheet-13",null=True, blank=True)
    TS_info14 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Tearsheet-14 info')
    TS_date14 = models.DateField("Fecha de Tearsheet-14",null=True, blank=True)
    TS_info15 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Tearsheet-15 info')
    TS_date15 = models.DateField("Fecha de Tearsheet-15",null=True, blank=True)
    TS_info16 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Tearsheet-16 info')
    TS_date16 = models.DateField("Fecha de Tearsheet-16",null=True, blank=True)
    TS_info17 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Tearsheet-17 info')
    TS_date17 = models.DateField("Fecha de Tearsheet-17",null=True, blank=True)
    TS_info18 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Tearsheet-18 info')
    TS_date18 = models.DateField("Fecha de Tearsheet-18",null=True, blank=True)
    TS_info19 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Tearsheet-19 info')
    TS_date19 = models.DateField("Fecha de Tearsheet-19",null=True, blank=True)
    TS_info20 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Tearsheet-20 info')
    TS_date20 = models.DateField("Fecha de Tearsheet-20",null=True, blank=True)
    
    #Campos de Noticias

    #template = "webapp_0/index.html"
    custom_title = models.CharField(max_length=100,blank=True,null=True,help_text="Reescribe el  Titulo de la publicacion ")


    
    # Campos de consulta

    consulta= RichTextField(blank=True,verbose_name='Mensaje para que nos consulten por el formulario')
    thank_you_text = RichTextField(blank=True)
    # galeria de imagenes barner de presentacion

    content_panels = AbstractEmailForm.content_panels + Page.content_panels + [

       # FieldPanel('title', classname="full"),
      #  FieldPanel('cliente_Navbar', classname="full"),
      #  FieldPanel('banner_info1', classname="full"),
      #  FieldPanel('banner_title2', classname="full"),
      #  FieldPanel('banner_info2', classname="full"),
      #  FieldPanel('banner_title3', classname="full"),
      #  FieldPanel('banner_info3', classname="full"),
    #Panel Gelerias
        FieldPanel('bio', classname="full"),
        FieldPanel('banner_title4', classname="full"),
        FieldPanel('banner_title5', classname="full"),
        FieldPanel('banner_title6', classname="full"),
        FieldPanel('banner_title7', classname="full"),
    #Tearsheet Info
        FieldPanel('TS_info1', classname="full"),
        FieldPanel('TS_date1', classname="full"),
        FieldPanel('TS_info2', classname="full"),
        FieldPanel('TS_date2', classname="full"),
        FieldPanel('TS_info3', classname="full"),
        FieldPanel('TS_date3', classname="full"),
        FieldPanel('TS_info4', classname="full"),
        FieldPanel('TS_date4', classname="full"),
        FieldPanel('TS_info5', classname="full"),
        FieldPanel('TS_date5', classname="full"),
        FieldPanel('TS_info6', classname="full"),
        FieldPanel('TS_date6', classname="full"),
        FieldPanel('TS_info7', classname="full"),
        FieldPanel('TS_date7', classname="full"),
        FieldPanel('TS_info8', classname="full"),
        FieldPanel('TS_date8', classname="full"),
        FieldPanel('TS_info9', classname="full"),
        FieldPanel('TS_date9', classname="full"),
        FieldPanel('TS_info10', classname="full"),
        FieldPanel('TS_date10', classname="full"),
        FieldPanel('TS_info11', classname="full"),
        FieldPanel('TS_date11', classname="full"),
        FieldPanel('TS_info12', classname="full"),
        FieldPanel('TS_date12', classname="full"),
        FieldPanel('TS_info13', classname="full"),
        FieldPanel('TS_date13', classname="full"),
        FieldPanel('TS_info14', classname="full"),
        FieldPanel('TS_date14', classname="full"),
        FieldPanel('TS_info15', classname="full"),
        FieldPanel('TS_date15', classname="full"),
        FieldPanel('TS_info16', classname="full"),
        FieldPanel('TS_date16', classname="full"),
        FieldPanel('TS_info17', classname="full"),
        FieldPanel('TS_date17', classname="full"),
        FieldPanel('TS_info18', classname="full"),
        FieldPanel('TS_date18', classname="full"),
        FieldPanel('TS_info19', classname="full"),
        FieldPanel('TS_date19', classname="full"),
        FieldPanel('TS_info20', classname="full"),
        FieldPanel('TS_date20', classname="full"),
#panel para campos de consulta
        FieldPanel('consulta', classname="full"),

        InlinePanel('galleria', label="Imagen de Fondo Barner"),
        InlinePanel('form_fields', label="consultas"),
        FieldPanel('thank_you_text', classname="full"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], "Email"),
#Panel capo de noticas
        FieldPanel("custom_title"),
    ]


        

class GaleriadeImagenes(Orderable):
    page = ParentalKey(Index, on_delete=models.CASCADE, related_name='galleria')
    logo = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Logotipo de Juan Silva Photo')
    profile_pic = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto de perfil')
    image = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 1')
    image_2 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 2')
    image_3 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 3')
    image_4_2 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 1')
    image_5_2 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 2')
    image_6_2 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 3')
    image_7_2 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 1')
    image_8_2 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 2')
    image_9_2 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 3')
    image_10_2 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 3')
    
    # Imagenes Thumb Portfolio
    
    image_4 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Advertising Thumb-Galeria')
    image_5 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Product Thumb2-Galeria')
    image_6 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Documentary Thumb3-Galeria')
    image_7 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Landscape Thumb4-Galeria')

    # Fotos TearSheate
    image_8 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Tear-Sheet-1')
    image_9 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Tear-Sheet-2')
    image_10 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Tear-Sheet-3')
    image_11 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Tear-Sheet-4')
    image_12 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Tear-Sheet-5 ')
    image_13 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Tear-Sheet-6')
    image_14 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Tear-Sheet-7')
    image_15 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Tear-Sheet-8')
    image_16 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Tear-Sheet-9')
    image_17 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Tear-Sheet-10')
    image_18 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Tear-Sheet-11')
    image_19 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Tear-Sheet-12')
    image_20 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Tear-Sheet-13')
    image_21 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Tear-Sheet-14')
    image_22 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Tear-Sheet-15')
    image_23 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Tear-Sheet-16')
    image_24 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Tear-Sheet-17')
    image_25 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Tear-Sheet-18')
    image_26 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Tear-Sheet-19')
    image_27 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Tear-Sheet-20')
    
    panels = [
    FieldPanel('logo'),
    FieldPanel('profile_pic'),
    FieldPanel('image'),
    FieldPanel('image_2'),
    FieldPanel('image_3'),
    FieldPanel('image_4_2'),
    FieldPanel('image_5_2'),
    FieldPanel('image_6_2'),
    FieldPanel('image_7_2'),
    FieldPanel('image_8_2'),
    FieldPanel('image_9_2'),
    FieldPanel('image_10_2'),
    FieldPanel('image_4'),
    FieldPanel('image_5'),
    FieldPanel('image_6'),
    FieldPanel('image_7'),
    FieldPanel('image_8'),
    FieldPanel('image_9'),
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
    FieldPanel('image_27'),
]


class consultas_advertising(AbstractFormField):
    page = ParentalKey('Advertising', on_delete=models.CASCADE, related_name='form_fields')

class Advertising(AbstractEmailForm):
    # Empieza Galeria de Imagenes
    template = "webapp_0/advertising.html"
   
    Ad_info = RichTextField(blank=True,verbose_name='Informacion de la Galeria',null=True)
    Ad_author = models.CharField(max_length=150, null=True, blank=True,verbose_name='Author')
    Ad_art =  models.CharField(max_length=150, null=True, blank=True,verbose_name='Direccion de arte')
    Ad_styling =  models.CharField(max_length=150, null=True, blank=True,verbose_name='Styling')
    Ad_retouching =  models.CharField(max_length=150, null=True, blank=True,verbose_name='retouching')
    Ad_agency=  models.CharField(max_length=150, null=True, blank=True,verbose_name='agency')
    Ad_camera =  models.CharField(max_length=150, null=True, blank=True,verbose_name='Camera')
    Ad_link = RichTextField(blank=True,verbose_name='Enlace para volver al inicio')
    
    consulta= RichTextField(blank=True,verbose_name='Mensaje para que nos consulten por el formulario')
    thank_you_text = RichTextField(blank=True)
    
    
    
    content_panels = Page.content_panels + [
        FieldPanel('Ad_info', classname="full"),
        FieldPanel('Ad_author', classname="full"),
        FieldPanel('Ad_art', classname="full"),
        FieldPanel('Ad_styling', classname="full"),
        FieldPanel('Ad_retouching', classname="full"),
        FieldPanel('Ad_agency', classname="full"),
        FieldPanel('Ad_camera', classname="full"),
        FieldPanel('Ad_link', classname="full"),
       
        FieldPanel('consulta', classname="full"),
        InlinePanel('galleria_2', label="Imagen de Fondo Barner"),
        InlinePanel('form_fields', label="consultas"),
        FieldPanel('thank_you_text', classname="full"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], "Email"),
    ]  


    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        # If you need to show results only on landing page,
        # you may need check request.method

        results = dict()
        # Get information about form fields
        data_fields = [
            (field.clean_name, field.label)
            for field in self.get_form_fields()
        ]

        # Get all submissions for current page
        submissions = self.get_submission_class().objects.filter(page=self)
        for submission in submissions:
            data = submission.get_data()

            # Count results for each question
            for name, label in data_fields:
                answer = data.get(name)
                if answer is None:
                    # Something wrong with data.
                    # Probably you have changed questions
                    # and now we are receiving answers for old questions.
                    # Just skip them.
                    continue

                if type(answer) is list:
                    # Answer is a list if the field type is 'Checkboxes'
                    answer = u', '.join(answer)

                question_stats = results.get(label, {})
                question_stats[answer] = question_stats.get(answer, 0) + 1
                results[label] = question_stats

        context.update({
            'results': results,
        })
        return context   
    

class GaleriadeImagenes2(Orderable):
    page = ParentalKey(Advertising, on_delete=models.CASCADE, related_name='galleria_2')
    logo = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Logotipo de Juan Silva Photo')
    image = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 1')
    image_2 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 2')
    image_3 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 3')
    image_4 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 4')
    image_5 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 5')
    image_6 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 6')
    image_7 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 7')
    image_8 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 8')
    image_9 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 9')
    image_10 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 10')
    image_11 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 11')
    image_12 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 12 ')
    image_13 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 13')
    image_14 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 14')
    image_15 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 15')
    image_16 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 16')
    image_17 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 17')
    image_18 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 18')
    image_19 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 19')
    image_20 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 20')
    image_21 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 21')
    image_22 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 22')
    image_23 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 23')
    image_24 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 24')
    image_25 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 25')
    image_26 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 26')
    image_27 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 27')
    image_28 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 28')
    image_29 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 29')
    image_30 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 30')
    image_31 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 31')
    image_32 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 32')
    image_33 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 33')
    image_34 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 34')
    image_35 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 35')
    image_36 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 36')
    image_37 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 37')
    image_38 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 38')
    image_39 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 39')
    image_40 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 40')
    image_41 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 41')
    image_42 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 42 ')
    image_43 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 43')
    image_44 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 44')
    image_45 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 45')
    image_46 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 46')
    image_47 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 47')
    image_48 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 48')
    image_49 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 49')
    image_50 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 50')
    image_51 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 51')
    image_52 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 52')
    image_53 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 53')
    image_54 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 54')
    image_55 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 55')
    image_56 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 56')
    image_57 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 57')
    image_58 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 58')
    image_59 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 59')
    image_60 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 60')

    consulta= RichTextField(blank=True,verbose_name='Mensaje para que nos consulten por el formulario')
    thank_you_text = RichTextField(blank=True)
     
    panels = [
    FieldPanel('logo'),
    FieldPanel('image'),
    FieldPanel('image_2'),
    FieldPanel('image_3'),
    FieldPanel('image_4'),
    FieldPanel('image_5'),
    FieldPanel('image_6'),
    FieldPanel('image_7'),
    FieldPanel('image_8'),
    FieldPanel('image_9'),
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
    FieldPanel('image_27'),
    FieldPanel('image_28'),
    FieldPanel('image_29'),
    FieldPanel('image_30'),
    FieldPanel('image_31'),
    FieldPanel('image_32'),
    FieldPanel('image_33'),
    FieldPanel('image_34'),
    FieldPanel('image_35'),
    FieldPanel('image_36'),
    FieldPanel('image_37'),
    FieldPanel('image_38'),
    FieldPanel('image_39'),
    FieldPanel('image_40'),
    FieldPanel('image_41'),
    FieldPanel('image_42'),
    FieldPanel('image_43'),
    FieldPanel('image_44'),
    FieldPanel('image_45'),
    FieldPanel('image_46'),
    FieldPanel('image_47'),
    FieldPanel('image_48'),
    FieldPanel('image_49'),
    FieldPanel('image_50'),
    FieldPanel('image_51'),
    FieldPanel('image_52'),
    FieldPanel('image_53'),
    FieldPanel('image_54'),
    FieldPanel('image_55'),
    FieldPanel('image_56'),
    FieldPanel('image_57'),
    FieldPanel('image_58'),
    FieldPanel('image_59'),
    FieldPanel('image_60'),
]



@register_setting
class SocialMediaSettings(BaseSiteSetting):
    facebook = models.URLField(blank=True,null=True,help_text="")
    twitter = models.URLField(blank=True,null=True,help_text="")
    instagram = models.URLField(blank=True,null=True,help_text="")
    youtube = models.URLField(blank=True,null=True,help_text="")
    behance = models.URLField(blank=True,null=True,help_text="")
    linkedin = models.URLField(blank=True,null=True,help_text="")

    panels = [
        MultiFieldPanel(
            [
            FieldPanel("facebook"),
            FieldPanel("twitter"),
            FieldPanel("instagram"),
            FieldPanel("youtube"),  
            FieldPanel("behance"),
            FieldPanel("linkedin"),         
            ]
        ,heading= "Social Media Settings")
    ]



class consultas_Prod(AbstractFormField):
    page = ParentalKey('Productos', on_delete=models.CASCADE, related_name='form_fields')

class Productos(AbstractEmailForm):
    # Empieza Galeria de Imagenes
    template = "webapp_0/products.html"
    Ad_info = RichTextField(blank=True,verbose_name='Informacion de la Galeria',null=True)
    Ad_author = models.CharField(max_length=150, null=True, blank=True,verbose_name='Author')
    Ad_art =  models.CharField(max_length=150, null=True, blank=True,verbose_name='Direccion de arte')
    Ad_styling =  models.CharField(max_length=150, null=True, blank=True,verbose_name='Styling')
    Ad_retouching =  models.CharField(max_length=150, null=True, blank=True,verbose_name='retouching')
    Ad_agency=  models.CharField(max_length=150, null=True, blank=True,verbose_name='agency')
    Ad_camera =  models.CharField(max_length=150, null=True, blank=True,verbose_name='Camera')
    Ad_link = RichTextField(blank=True,verbose_name='Enlace para volver al inicio')
    
    consulta= RichTextField(blank=True,verbose_name='Mensaje para que nos consulten por el formulario')
    thank_you_text = RichTextField(blank=True)
    
    
    
    content_panels = Page.content_panels + [
        FieldPanel('Ad_info', classname="full"),
        FieldPanel('Ad_author', classname="full"),
        FieldPanel('Ad_art', classname="full"),
        FieldPanel('Ad_styling', classname="full"),
        FieldPanel('Ad_retouching', classname="full"),
        FieldPanel('Ad_agency', classname="full"),
        FieldPanel('Ad_camera', classname="full"),
        FieldPanel('Ad_link', classname="full"),
        FieldPanel('consulta', classname="full"),
        InlinePanel('galleria_3', label="Imagen de Fondo Barner"),
        InlinePanel('form_fields', label="consultas"),
        FieldPanel('thank_you_text', classname="full"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], "Email"),

    ]  


    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        # If you need to show results only on landing page,
        # you may need check request.method

        results = dict()
        # Get information about form fields
        data_fields = [
            (field.clean_name, field.label)
            for field in self.get_form_fields()
        ]

        # Get all submissions for current page
        submissions = self.get_submission_class().objects.filter(page=self)
        for submission in submissions:
            data = submission.get_data()

            # Count results for each question
            for name, label in data_fields:
                answer = data.get(name)
                if answer is None:
                    # Something wrong with data.
                    # Probably you have changed questions
                    # and now we are receiving answers for old questions.
                    # Just skip them.
                    continue

                if type(answer) is list:
                    # Answer is a list if the field type is 'Checkboxes'
                    answer = u', '.join(answer)

                question_stats = results.get(label, {})
                question_stats[answer] = question_stats.get(answer, 0) + 1
                results[label] = question_stats

        context.update({
            'results': results,
        })
        return context   

class GaleriadeImagenes3(Orderable):
    page = ParentalKey(Productos, on_delete=models.CASCADE, related_name='galleria_3')
    logo = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Logotipo de Juan Silva Photo')
    image = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 1')
    image_2 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 2')
    image_3 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 3')
    image_4 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 4')
    image_5 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 5')
    image_6 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 6')
    image_7 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 7')
    image_8 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 8')
    image_9 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 9')
    image_10 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 10')
    image_11 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 11')
    image_12 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 12 ')
    image_13 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 13')
    image_14 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 14')
    image_15 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 15')
    image_16 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 16')
    image_17 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 17')
    image_18 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 18')
    image_19 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 19')
    image_20 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 20')
    image_21 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 21')
    image_22 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 22')
    image_23 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 23')
    image_24 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 24')
    image_25 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 25')
    image_26 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 26')
    image_27 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 27')
    image_28 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 28')
    image_29 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 29')
    image_30 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 30')
    image_31 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 31')
    image_32 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 32')
    image_33 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 33')
    image_34 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 34')
    image_35 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 35')
    image_36 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 36')
    image_37 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 37')
    image_38 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 38')
    image_39 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 39')
    image_40 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 40')
    image_41 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 41')
    image_42 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 42 ')
    image_43 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 43')
    image_44 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 44')
    image_45 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 45')
    image_46 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 46')
    image_47 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 47')
    image_48 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 48')
    image_49 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 49')
    image_50 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 50')
    image_51 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 51')
    image_52 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 52')
    image_53 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 53')
    image_54 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 54')
    image_55 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 55')
    image_56 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 56')
    image_57 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 57')
    image_58 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 58')
    image_59 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 59')
    image_60 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 60')

    panels = [
    FieldPanel('logo'),
    FieldPanel('image'),
    FieldPanel('image_2'),
    FieldPanel('image_3'),
    FieldPanel('image_4'),
    FieldPanel('image_5'),
    FieldPanel('image_6'),
    FieldPanel('image_7'),
    FieldPanel('image_8'),
    FieldPanel('image_9'),
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
    FieldPanel('image_27'),
    FieldPanel('image_28'),
    FieldPanel('image_29'),
    FieldPanel('image_30'),
    FieldPanel('image_31'),
    FieldPanel('image_32'),
    FieldPanel('image_33'),
    FieldPanel('image_34'),
    FieldPanel('image_35'),
    FieldPanel('image_36'),
    FieldPanel('image_37'),
    FieldPanel('image_38'),
    FieldPanel('image_39'),
    FieldPanel('image_40'),
    FieldPanel('image_41'),
    FieldPanel('image_42'),
    FieldPanel('image_43'),
    FieldPanel('image_44'),
    FieldPanel('image_45'),
    FieldPanel('image_46'),
    FieldPanel('image_47'),
    FieldPanel('image_48'),
    FieldPanel('image_49'),
    FieldPanel('image_50'),
    FieldPanel('image_51'),
    FieldPanel('image_52'),
    FieldPanel('image_53'),
    FieldPanel('image_54'),
    FieldPanel('image_55'),
    FieldPanel('image_56'),
    FieldPanel('image_57'),
    FieldPanel('image_58'),
    FieldPanel('image_59'),
    FieldPanel('image_60'),
]

class consultas_Land(AbstractFormField):
    page = ParentalKey('Landscape', on_delete=models.CASCADE, related_name='form_fields')

class Landscape(AbstractEmailForm):
    template = "webapp_0/Landscape.html"
    # Empieza Galeria de Imagenes
    Ad_info = RichTextField(blank=True,verbose_name='Informacion de la Galeria',null=True)
    Ad_author = models.CharField(max_length=150, null=True, blank=True,verbose_name='Author')
    Ad_art =  models.CharField(max_length=150, null=True, blank=True,verbose_name='Direccion de arte')
    Ad_styling =  models.CharField(max_length=150, null=True, blank=True,verbose_name='Styling')
    Ad_retouching =  models.CharField(max_length=150, null=True, blank=True,verbose_name='retouching')
    Ad_agency=  models.CharField(max_length=150, null=True, blank=True,verbose_name='agency')
    Ad_camera =  models.CharField(max_length=150, null=True, blank=True,verbose_name='Camera')
    Ad_link = RichTextField(blank=True,verbose_name='Enlace para volver al inicio')
    
    consulta= RichTextField(blank=True,verbose_name='Mensaje para que nos consulten por el formulario')
    thank_you_text = RichTextField(blank=True)
    
    
    
    content_panels = Page.content_panels + [
        FieldPanel('Ad_info', classname="full"),
        FieldPanel('Ad_author', classname="full"),
        FieldPanel('Ad_art', classname="full"),
        FieldPanel('Ad_styling', classname="full"),
        FieldPanel('Ad_retouching', classname="full"),
        FieldPanel('Ad_agency', classname="full"),
        FieldPanel('Ad_camera', classname="full"),
        FieldPanel('Ad_link', classname="full"),
       
        FieldPanel('consulta', classname="full"),
        InlinePanel('galleria_4', label="Imagen de Fondo Barner"),
        InlinePanel('form_fields', label="consultas"),
        FieldPanel('thank_you_text', classname="full"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], "Email"),
    ]  


    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        # If you need to show results only on landing page,
        # you may need check request.method

        results = dict()
        # Get information about form fields
        data_fields = [
            (field.clean_name, field.label)
            for field in self.get_form_fields()
        ]

        # Get all submissions for current page
        submissions = self.get_submission_class().objects.filter(page=self)
        for submission in submissions:
            data = submission.get_data()

            # Count results for each question
            for name, label in data_fields:
                answer = data.get(name)
                if answer is None:
                    # Something wrong with data.
                    # Probably you have changed questions
                    # and now we are receiving answers for old questions.
                    # Just skip them.
                    continue

                if type(answer) is list:
                    # Answer is a list if the field type is 'Checkboxes'
                    answer = u', '.join(answer)

                question_stats = results.get(label, {})
                question_stats[answer] = question_stats.get(answer, 0) + 1
                results[label] = question_stats

        context.update({
            'results': results,
        })
        return context   

class GaleriadeImagenes4(Orderable):
    page = ParentalKey(Landscape, on_delete=models.CASCADE, related_name='galleria_4')
    logo = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Logotipo de Juan Silva Photo')
    image = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 1')
    image_2 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 2')
    image_3 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 3')
    image_4 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 4')
    image_5 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 5')
    image_6 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 6')
    image_7 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 7')
    image_8 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 8')
    image_9 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 9')
    image_10 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 10')
    image_11 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 11')
    image_12 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 12 ')
    image_13 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 13')
    image_14 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 14')
    image_15 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 15')
    image_16 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 16')
    image_17 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 17')
    image_18 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 18')
    image_19 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 19')
    image_20 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 20')
    image_21 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 21')
    image_22 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 22')
    image_23 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 23')
    image_24 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 24')
    image_25 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 25')
    image_26 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 26')
    image_27 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 27')
    image_28 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 28')
    image_29 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 29')
    image_30 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 30')
    image_31 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 31')
    image_32 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 32')
    image_33 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 33')
    image_34 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 34')
    image_35 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 35')
    image_36 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 36')
    image_37 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 37')
    image_38 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 38')
    image_39 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 39')
    image_40 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 40')
    image_41 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 41')
    image_42 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 42 ')
    image_43 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 43')
    image_44 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 44')
    image_45 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 45')
    image_46 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 46')
    image_47 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 47')
    image_48 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 48')
    image_49 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 49')
    image_50 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 50')
    image_51 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 51')
    image_52 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 52')
    image_53 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 53')
    image_54 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 54')
    image_55 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 55')
    image_56 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 56')
    image_57 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 57')
    image_58 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 58')
    image_59 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 59')
    image_60 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 60')
     

    panels = [
    FieldPanel('logo'),
    FieldPanel('image'),
    FieldPanel('image_2'),
    FieldPanel('image_3'),
    FieldPanel('image_4'),
    FieldPanel('image_5'),
    FieldPanel('image_6'),
    FieldPanel('image_7'),
    FieldPanel('image_8'),
    FieldPanel('image_9'),
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
    FieldPanel('image_27'),
    FieldPanel('image_28'),
    FieldPanel('image_29'),
    FieldPanel('image_30'),
    FieldPanel('image_31'),
    FieldPanel('image_32'),
    FieldPanel('image_33'),
    FieldPanel('image_34'),
    FieldPanel('image_35'),
    FieldPanel('image_36'),
    FieldPanel('image_37'),
    FieldPanel('image_38'),
    FieldPanel('image_39'),
    FieldPanel('image_40'),
    FieldPanel('image_41'),
    FieldPanel('image_42'),
    FieldPanel('image_43'),
    FieldPanel('image_44'),
    FieldPanel('image_45'),
    FieldPanel('image_46'),
    FieldPanel('image_47'),
    FieldPanel('image_48'),
    FieldPanel('image_49'),
    FieldPanel('image_50'),
    FieldPanel('image_51'),
    FieldPanel('image_52'),
    FieldPanel('image_53'),
    FieldPanel('image_54'),
    FieldPanel('image_55'),
    FieldPanel('image_56'),
    FieldPanel('image_57'),
    FieldPanel('image_58'),
    FieldPanel('image_59'),
    FieldPanel('image_60'),
]

class consultas_Doc(AbstractFormField):
    page = ParentalKey('Documentary', on_delete=models.CASCADE, related_name='form_fields')

class Documentary(AbstractEmailForm):
    # Empieza Galeria de Imagenes
    template = "webapp_0/Documentary.html"
    
    Ad_info = RichTextField(blank=True,verbose_name='Informacion de la Galeria',null=True)
    Ad_author = models.CharField(max_length=150, null=True, blank=True,verbose_name='Author')
    Ad_art =  models.CharField(max_length=150, null=True, blank=True,verbose_name='Direccion de arte')
    Ad_styling =  models.CharField(max_length=150, null=True, blank=True,verbose_name='Styling')
    Ad_retouching =  models.CharField(max_length=150, null=True, blank=True,verbose_name='retouching')
    Ad_agency=  models.CharField(max_length=150, null=True, blank=True,verbose_name='agency')
    Ad_camera =  models.CharField(max_length=150, null=True, blank=True,verbose_name='Camera')
    Ad_link = RichTextField(blank=True,verbose_name='Enlace para volver al inicio')
    
    consulta= RichTextField(blank=True,verbose_name='Mensaje para que nos consulten por el formulario')
    thank_you_text = RichTextField(blank=True)
    
    
    
    content_panels = Page.content_panels + [
        FieldPanel('Ad_info', classname="full"),
        FieldPanel('Ad_author', classname="full"),
        FieldPanel('Ad_art', classname="full"),
        FieldPanel('Ad_styling', classname="full"),
        FieldPanel('Ad_retouching', classname="full"),
        FieldPanel('Ad_agency', classname="full"),
        FieldPanel('Ad_camera', classname="full"),
        FieldPanel('Ad_link', classname="full"),
       
        FieldPanel('consulta', classname="full"),
        InlinePanel('galleria_5', label="Imagen de Fondo Barner"),
        InlinePanel('form_fields', label="consultas"),
        FieldPanel('thank_you_text', classname="full"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], "Email"),
    ]  


    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        # If you need to show results only on landing page,
        # you may need check request.method

        results = dict()
        # Get information about form fields
        data_fields = [
            (field.clean_name, field.label)
            for field in self.get_form_fields()
        ]

        # Get all submissions for current page
        submissions = self.get_submission_class().objects.filter(page=self)
        for submission in submissions:
            data = submission.get_data()

            # Count results for each question
            for name, label in data_fields:
                answer = data.get(name)
                if answer is None:
                    # Something wrong with data.
                    # Probably you have changed questions
                    # and now we are receiving answers for old questions.
                    # Just skip them.
                    continue

                if type(answer) is list:
                    # Answer is a list if the field type is 'Checkboxes'
                    answer = u', '.join(answer)

                question_stats = results.get(label, {})
                question_stats[answer] = question_stats.get(answer, 0) + 1
                results[label] = question_stats

        context.update({
            'results': results,
        })
        return context   

class GaleriadeImagenes5(Orderable):
    page = ParentalKey(Documentary, on_delete=models.CASCADE, related_name='galleria_5')
    logo = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Logotipo de Juan Silva Photo')
    image = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 1')
    image_2 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 2')
    image_3 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 3')
    image_4 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 4')
    image_5 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 5')
    image_6 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 6')
    image_7 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 7')
    image_8 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 8')
    image_9 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 9')
    image_10 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 10')
    image_11 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 11')
    image_12 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 12 ')
    image_13 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 13')
    image_14 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 14')
    image_15 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 15')
    image_16 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 16')
    image_17 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 17')
    image_18 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 18')
    image_19 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 19')
    image_20 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 20')
    image_21 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 21')
    image_22 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 22')
    image_23 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 23')
    image_24 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 24')
    image_25 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 25')
    image_26 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 26')
    image_27 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 27')
    image_28 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 28')
    image_29 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 29')
    image_30 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 30')
    image_31 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 31')
    image_32 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 32')
    image_33 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 33')
    image_34 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 34')
    image_35 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 35')
    image_36 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 36')
    image_37 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 37')
    image_38 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 38')
    image_39 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 39')
    image_40 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 40')
    image_41 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 41')
    image_42 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 42 ')
    image_43 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 43')
    image_44 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 44')
    image_45 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 45')
    image_46 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 46')
    image_47 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 47')
    image_48 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 48')
    image_49 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 49')
    image_50 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 50')
    image_51 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 51')
    image_52 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 52')
    image_53 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 53')
    image_54 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 54')
    image_55 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 55')
    image_56 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 56')
    image_57 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 57')
    image_58 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 58')
    image_59 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 59')
    image_60 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 60')
     

    panels = [
    FieldPanel('logo'),
    FieldPanel('image'),
    FieldPanel('image_2'),
    FieldPanel('image_3'),
    FieldPanel('image_4'),
    FieldPanel('image_5'),
    FieldPanel('image_6'),
    FieldPanel('image_7'),
    FieldPanel('image_8'),
    FieldPanel('image_9'),
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
    FieldPanel('image_27'),
    FieldPanel('image_28'),
    FieldPanel('image_29'),
    FieldPanel('image_30'),
    FieldPanel('image_31'),
    FieldPanel('image_32'),
    FieldPanel('image_33'),
    FieldPanel('image_34'),
    FieldPanel('image_35'),
    FieldPanel('image_36'),
    FieldPanel('image_37'),
    FieldPanel('image_38'),
    FieldPanel('image_39'),
    FieldPanel('image_40'),
    FieldPanel('image_41'),
    FieldPanel('image_42'),
    FieldPanel('image_43'),
    FieldPanel('image_44'),
    FieldPanel('image_45'),
    FieldPanel('image_46'),
    FieldPanel('image_47'),
    FieldPanel('image_48'),
    FieldPanel('image_49'),
    FieldPanel('image_50'),
    FieldPanel('image_51'),
    FieldPanel('image_52'),
    FieldPanel('image_53'),
    FieldPanel('image_54'),
    FieldPanel('image_55'),
    FieldPanel('image_56'),
    FieldPanel('image_57'),
    FieldPanel('image_58'),
    FieldPanel('image_59'),
    FieldPanel('image_60'),
]


class consultas_tear(AbstractFormField):
    page = ParentalKey('Tearsheeting', on_delete=models.CASCADE, related_name='form_fields')

class Tearsheeting(AbstractEmailForm):
    # Empieza Galeria de Imagenes
    template = "webapp_0/tearsheeting.html"
    
    Ad_info = RichTextField(blank=True,verbose_name='Informacion de la Galeria',null=True)
    Ad_author = models.CharField(max_length=150, null=True, blank=True,verbose_name='Author')
    Ad_art =  models.CharField(max_length=150, null=True, blank=True,verbose_name='Direccion de arte')
    Ad_styling =  models.CharField(max_length=150, null=True, blank=True,verbose_name='Styling')
    Ad_retouching =  models.CharField(max_length=150, null=True, blank=True,verbose_name='retouching')
    Ad_agency=  models.CharField(max_length=150, null=True, blank=True,verbose_name='agency')
    Ad_camera =  models.CharField(max_length=150, null=True, blank=True,verbose_name='Camera')
    Ad_link = RichTextField(blank=True,verbose_name='Enlace para volver al inicio')
    
    consulta= RichTextField(blank=True,verbose_name='Mensaje para que nos consulten por el formulario')
    thank_you_text = RichTextField(blank=True)
    
    
    
    content_panels = Page.content_panels + [
        FieldPanel('Ad_info', classname="full"),
        FieldPanel('Ad_author', classname="full"),
        FieldPanel('Ad_art', classname="full"),
        FieldPanel('Ad_styling', classname="full"),
        FieldPanel('Ad_retouching', classname="full"),
        FieldPanel('Ad_agency', classname="full"),
        FieldPanel('Ad_camera', classname="full"),
        FieldPanel('Ad_link', classname="full"),
       
        FieldPanel('consulta', classname="full"),
        InlinePanel('galleria_6', label="Imagen de Fondo Barner"),
        InlinePanel('form_fields', label="consultas"),
        FieldPanel('thank_you_text', classname="full"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], "Email"),
    ]  


    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        # If you need to show results only on landing page,
        # you may need check request.method

        results = dict()
        # Get information about form fields
        data_fields = [
            (field.clean_name, field.label)
            for field in self.get_form_fields()
        ]

        # Get all submissions for current page
        submissions = self.get_submission_class().objects.filter(page=self)
        for submission in submissions:
            data = submission.get_data()

            # Count results for each question
            for name, label in data_fields:
                answer = data.get(name)
                if answer is None:
                    # Something wrong with data.
                    # Probably you have changed questions
                    # and now we are receiving answers for old questions.
                    # Just skip them.
                    continue

                if type(answer) is list:
                    # Answer is a list if the field type is 'Checkboxes'
                    answer = u', '.join(answer)

                question_stats = results.get(label, {})
                question_stats[answer] = question_stats.get(answer, 0) + 1
                results[label] = question_stats

        context.update({
            'results': results,
        })
        return context   

class GaleriadeImagenes6(Orderable):
    page = ParentalKey(Tearsheeting, on_delete=models.CASCADE, related_name='galleria_6')
    logo = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Logotipo de Juan Silva Photo')
    image = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 1')
    image_2 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 2')
    image_3 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 3')
    image_4 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 4')
    image_5 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 5')
    image_6 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 6')
    image_7 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 7')
    image_8 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 8')
    image_9 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 9')
    image_10 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 10')
    image_11 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 11')
    image_12 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 12 ')
    image_13 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 13')
    image_14 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 14')
    image_15 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 15')
    image_16 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 16')
    image_17 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 17')
    image_18 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 18')
    image_19 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 19')
    image_20 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 20')
    image_21 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 21')
    image_22 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 22')
    image_23 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 23')
    image_24 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 24')
    image_25 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 25')
    image_26 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 26')
    image_27 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 27')
    image_28 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 28')
    image_29 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 29')
    image_30 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 30')
    image_31 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 31')
    image_32 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 32')
    image_33 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 33')
    image_34 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 34')
    image_35 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 35')
    image_36 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 36')
    image_37 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 37')
    image_38 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 38')
    image_39 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 39')
    image_40 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 40')
    image_41 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 41')
    image_42 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 42 ')
    image_43 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 43')
    image_44 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 44')
    image_45 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 45')
    image_46 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 46')
    image_47 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 47')
    image_48 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 48')
    image_49 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 49')
    image_50 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 50')
    image_51 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 51')
    image_52 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 52')
    image_53 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 53')
    image_54 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 54')
    image_55 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 55')
    image_56 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 56')
    image_57 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 57')
    image_58 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 58')
    image_59 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 59')
    image_60 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 60')
     

    panels = [
    FieldPanel('logo'),
    FieldPanel('image'),
    FieldPanel('image_2'),
    FieldPanel('image_3'),
    FieldPanel('image_4'),
    FieldPanel('image_5'),
    FieldPanel('image_6'),
    FieldPanel('image_7'),
    FieldPanel('image_8'),
    FieldPanel('image_9'),
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
    FieldPanel('image_27'),
    FieldPanel('image_28'),
    FieldPanel('image_29'),
    FieldPanel('image_30'),
    FieldPanel('image_31'),
    FieldPanel('image_32'),
    FieldPanel('image_33'),
    FieldPanel('image_34'),
    FieldPanel('image_35'),
    FieldPanel('image_36'),
    FieldPanel('image_37'),
    FieldPanel('image_38'),
    FieldPanel('image_39'),
    FieldPanel('image_40'),
    FieldPanel('image_41'),
    FieldPanel('image_42'),
    FieldPanel('image_43'),
    FieldPanel('image_44'),
    FieldPanel('image_45'),
    FieldPanel('image_46'),
    FieldPanel('image_47'),
    FieldPanel('image_48'),
    FieldPanel('image_49'),
    FieldPanel('image_50'),
    FieldPanel('image_51'),
    FieldPanel('image_52'),
    FieldPanel('image_53'),
    FieldPanel('image_54'),
    FieldPanel('image_55'),
    FieldPanel('image_56'),
    FieldPanel('image_57'),
    FieldPanel('image_58'),
    FieldPanel('image_59'),
    FieldPanel('image_60'),
]


class about_recomend(AbstractFormField):
    page = ParentalKey('About', on_delete=models.CASCADE, related_name='form_fields')

class About(AbstractEmailForm):
    # Empieza Galeria de Imagenes
    template = "webapp_0/about.html"
    
    About_info = RichTextField(blank=True,verbose_name='Quien eres?')
    About_info2 = RichTextField(blank=True,verbose_name='Cual es tu trayectoria profesional')
    finish_projects = models.IntegerField(verbose_name='Numero de proyectos terminados') 
    countrys_projects = models.IntegerField(verbose_name='Numero Paises donde se trabajo') 
    agencies_projects = models.IntegerField(verbose_name='Numero de agencias contratadas')
    hours_projects = models.IntegerField(verbose_name='Horas de trabajo totales')

    skilis1 =  models.CharField(max_length=150, null=True, blank=True,verbose_name='Programa de edicion y prodeccion fotografica-1')
    pskilis1 = models.IntegerField(verbose_name='Porcentaje de abilidad del Programa-1')
    

    skilis2 =  models.CharField(max_length=150, null=True, blank=True,verbose_name='Programa de edicion y prodeccion fotografica-2')
    pskilis2 = models.IntegerField(verbose_name='Porcentaje de abilidad del Programa-2')
    
    skilis3 =  models.CharField(max_length=150, null=True, blank=True,verbose_name='Programa de edicion y prodeccion fotografica-2')
    pskilis3 =  models.IntegerField(verbose_name='Porcentaje de abilidad del Programa-3')

    skilis4 =  models.CharField(max_length=150, null=True, blank=True,verbose_name='Programa de edicion y prodeccion fotografica-3')
    pskilis4 =  models.IntegerField(verbose_name='Porcentaje de abilidad del Programa-4')

    
    consulta= RichTextField(blank=True,verbose_name='Mensaje para que nos consulten por el formulario')
    thank_you_text = RichTextField(blank=True)
    
    
    
    content_panels = Page.content_panels + [
        FieldPanel('About_info', classname="full"),
        FieldPanel('About_info2', classname="full"),
        FieldPanel('finish_projects', classname="full"),
        FieldPanel('countrys_projects', classname="full"),
        FieldPanel('agencies_projects', classname="full"),
        FieldPanel('hours_projects', classname="full"),
        FieldPanel('skilis1', classname="full"),
        FieldPanel('pskilis1', classname="full"),
        FieldPanel('skilis2', classname="full"),
        FieldPanel('pskilis2', classname="full"),
        FieldPanel('skilis3', classname="full"),
        FieldPanel('pskilis3', classname="full"),
        FieldPanel('skilis4', classname="full"),
        FieldPanel('pskilis4', classname="full"),
       
        FieldPanel('consulta', classname="full"),
        InlinePanel('galleria_7', label="Imagen de Fondo Barner"),
        InlinePanel('form_fields', label="consultas"),
        FieldPanel('thank_you_text', classname="full"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], "Email"),
    ]  

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["abouts"] = About.objects.live().public()
        return context


    
class GaleriadeImagenes7(Orderable):
    page = ParentalKey(About, on_delete=models.CASCADE, related_name='galleria_7')
    logo = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Logotipo de Juan Silva Photo')
    image = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto 1')   

    panels = [
        FieldPanel('logo'),
        FieldPanel('image'),
    ]


