# pagina de inicio
class consultas(AbstractFormField):
    page = ParentalKey('smartbusinessmedia', on_delete=models.CASCADE, related_name='form_fields')

class smartbusinessmedia(AbstractEmailForm):
    # Empieza Barner de Inicio
    template = "webapp/products/smartbusinessmedia/index/smartbusinesmedia.html"
    #cliente_Navbar = RichTextField(blank=True,verbose_name='Cliente-url')
    
   # banner_title1 = RichTextField(blank=True,verbose_name='Titulo del primer banner ')
   # banner_info1 = RichTextField(blank=True,verbose_name='Informacion del primer banner ')
   # banner_title2 = RichTextField(blank=True,verbose_name='Titulo del segundo banner ')
   # banner_info2 = RichTextField(blank=True,verbose_name='Informacion del segundo banner ')
   # banner_title3 = RichTextField(blank=True,verbose_name='Titulo del tercer banner ')
   # banner_info3 = RichTextField(blank=True,verbose_name='Informacion del tercer banner ')

    # Empieza Banner de sliders
    bio = RichTextField(blank=True,verbose_name='rseña bibliografica')

    banner_title4 = RichTextField(blank=True,verbose_name='Titulo de galeria-1 ')
    TS_info1 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Subtitulo info')
    info1 = models.CharField(max_length=150, null=True, blank=True,verbose_name='info')
    banner_title5 = RichTextField(blank=True,verbose_name='Titulo de galeria-2  ')
    TS_info2 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Subtitulo-2 info')
    info2 = models.CharField(max_length=150, null=True, blank=True,verbose_name='info-2')
    banner_title6 = RichTextField(blank=True,verbose_name='Titulo de galeria-3  ')
    TS_info3 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Subtitulo-3 info')
    info3 = models.CharField(max_length=150, null=True, blank=True,verbose_name='info-3')
    banner_title7 = RichTextField(blank=True,verbose_name='Titulo de galeria-4  ')
    TS_info4 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Subtitulot-4 info')
    info4 = models.CharField(max_length=150, null=True, blank=True,verbose_name='info-4')
    banner_title8 = RichTextField(blank=True,verbose_name='Titulo de galeria-5  ')
    TS_info5 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Subtitulo-5 info')
    info5 = models.CharField(max_length=150, null=True, blank=True,verbose_name='info-5')
    banner_title9 = RichTextField(blank=True,verbose_name='Titulo de galeria-6  ')
    TS_info6 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Subtitulo-6 info')
    info6 = models.CharField(max_length=150, null=True, blank=True,verbose_name='info-6')


    # Empieza Banner de callout
    banner_title10 = RichTextField(blank=True,verbose_name='we improve')
    info7 = models.CharField(max_length=150, null=True, blank=True,verbose_name='IT business analytics')
    info8 = models.CharField(max_length=150, null=True, blank=True,verbose_name='IT business cloud DevOps')
    info9 = models.CharField(max_length=150, null=True, blank=True,verbose_name='IT business Media')
    
    # Empieza Banner de Products

  
    product_1 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Product-1')
    product_description_1 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Descripcion Product-1')
    product_2 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Product-2')
    product_description_2 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Descripcion Product-2')
    product_3 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Product-3')
    product_description_3 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Descripcion Product-3')
    product_4 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Product-4')
    product_description_4 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Descripcion Product-4')
    product_5 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Product-5')
    product_description_5 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Descripcion Product-5')
    product_6 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Product-6')
    product_description_6 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Descripcion Product-6')
    # Banner contador
    numero_coffe = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    numero_experiencia = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    numero_horas = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    numero_wins = models.DecimalField(max_digits=10, decimal_places=2,null=True)


    team_1 = models.CharField(max_length=150, null=True, blank=True,verbose_name='team-1')
    team_descrp_1 = models.CharField(max_length=150, null=True, blank=True,verbose_name='team descripcion-1')
    team_2 = models.CharField(max_length=150, null=True, blank=True,verbose_name='team-2')
    team_descrp_2 = models.CharField(max_length=150, null=True, blank=True,verbose_name='team descripcion-2')
    team_3 = models.CharField(max_length=150, null=True, blank=True,verbose_name='team-3')
    team_descrp_3 = models.CharField(max_length=150, null=True, blank=True,verbose_name='team descripcion-3')
    team_4 = models.CharField(max_length=150, null=True, blank=True,verbose_name='team-4')
    team_descrp_4 = models.CharField(max_length=150, null=True, blank=True,verbose_name='team descripcion-4')

    banner_title = models.CharField(max_length=150, null=True, blank=True,verbose_name='Call Action Title')
    slogan = models.CharField(max_length=150, null=True, blank=True,verbose_name='slogan')
    slogan_descriptcion = models.CharField(max_length=150, null=True, blank=True,verbose_name='slogan Description')
    


    custom_title = models.CharField(max_length=100,blank=True,null=True,help_text="Reescribe el  Titulo de la publicacion ")


    
    # Campos de consulta

    consulta= RichTextField(blank=True,verbose_name='Mensaje para que nos consulten por el formulario')
    thank_you_text = RichTextField(blank=True)
    # galeria de imagenes barner de presentacion

    content_panels = AbstractEmailForm.content_panels + Page.content_panels + [


    #Panel sliders
        FieldPanel('bio', classname="full"),
        FieldPanel('banner_title4', classname="full"),
        FieldPanel('TS_info1', classname="full"),
        FieldPanel('info1', classname="full"),
        FieldPanel('banner_title5', classname="full"),
        FieldPanel('TS_info2', classname="full"),
        FieldPanel('info2', classname="full"),
        FieldPanel('banner_title6', classname="full"),
        FieldPanel('TS_info3', classname="full"),
        FieldPanel('info3', classname="full"),
        FieldPanel('banner_title7', classname="full"),
        FieldPanel('TS_info4', classname="full"),
        FieldPanel('info4', classname="full"),
        FieldPanel('banner_title8', classname="full"),
        FieldPanel('TS_info5', classname="full"),
        FieldPanel('info5', classname="full"),
        FieldPanel('banner_title9', classname="full"),
        FieldPanel('TS_info6', classname="full"),
        FieldPanel('info6', classname="full"),
        FieldPanel('banner_title10', classname="full"),
        FieldPanel('info7', classname="full"),
        FieldPanel('info8', classname="full"),
        FieldPanel('info9', classname="full"),


        FieldPanel('product_1', classname="full"),
        FieldPanel('product_description_1', classname="full"),
        FieldPanel('product_2', classname="full"),
        FieldPanel('product_description_2', classname="full"),
        FieldPanel('product_3', classname="full"),
        FieldPanel('product_description_3', classname="full"),
        FieldPanel('product_4', classname="full"),
        FieldPanel('product_description_4', classname="full"),
        FieldPanel('product_5', classname="full"),
        FieldPanel('product_description_5', classname="full"),
        FieldPanel('product_6', classname="full"),
        FieldPanel('product_description_6', classname="full"),
        FieldPanel('numero_coffe', classname="full"),
        FieldPanel('numero_experiencia', classname="full"),
        FieldPanel('numero_horas', classname="full"),
        FieldPanel('numero_wins', classname="full"),
        FieldPanel('team_1', classname="full"),
        FieldPanel('team_descrp_1', classname="full"),
        FieldPanel('team_2', classname="full"),
        FieldPanel('team_descrp_2', classname="full"),
        FieldPanel('team_3', classname="full"),
        FieldPanel('team_descrp_3', classname="full"),
        FieldPanel('team_4', classname="full"),
        FieldPanel('team_descrp_4', classname="full"),
        FieldPanel('banner_title', classname="full"),
        FieldPanel('slogan', classname="full"),
        FieldPanel('slogan_descriptcion', classname="full"),


#panel 
        FieldPanel('consulta', classname="full"),

        InlinePanel('galleria_2', label="Imagen de Fondo Barner"),
        FormSubmissionsPanel(),
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



class GaleriadeImagenesSBM(Orderable):
    page = ParentalKey(smartbusinessmedia, on_delete=models.CASCADE, related_name='galleria_2')
    logo = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Logotipo SmartQuail')
    profile_pic = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto de perfil')
    image = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 1')
    image_2 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 2')
    image_3 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 3')
    image_4 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 4')
    image_5 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 5')
    image_6 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 6')
    image_7 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen product 1')
    image_8 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen product 2')
    image_9 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen product 3')
    image_10 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen product 4')
    image_11 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen product 5')
    image_12 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen product 6')
    image_13 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen team 1')
    image_14 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen team 2')
    image_15 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen team 3')
    image_16 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen team 4')

    panels = [
        ImageChooserPanel('logo'),
        ImageChooserPanel('profile_pic'),
        ImageChooserPanel('image'),
        ImageChooserPanel('image_2'),
        ImageChooserPanel('image_3'),
        ImageChooserPanel('image_4'),
        ImageChooserPanel('image_5'),
        ImageChooserPanel('image_6'),
        ImageChooserPanel('image_7'),
        ImageChooserPanel('image_8'),
        ImageChooserPanel('image_9'),
        ImageChooserPanel('image_10'),
        ImageChooserPanel('image_11'),
        ImageChooserPanel('image_12'),
        ImageChooserPanel('image_13'),
        ImageChooserPanel('image_14'),
        ImageChooserPanel('image_15'),
        ImageChooserPanel('image_16'),
    ]




class Category(models.Model):
    name = models.CharField(max_length=200,
                            db_index=True)
    slug = models.SlugField(max_length=200,
                            unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
            return reverse('shop:product_list_by_category',
                           args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(Category,
                                 related_name='products',
                                 on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d',
                              blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
            return reverse('shop:product_detail',
                           args=[self.id, self.slug])




class info(Page):
    # Empieza Barner de Inicio
    template = "webapp/info.html"
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

    content_panels = AbstractEmailForm.content_panels + Page.content_panels + [


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
    image_1 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 1')
    image_2_2 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 1')
    image_2 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 2')
    image_3_3 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 1')

    image_3 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 3')
    image_4_4 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 1')
    image_4 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 4')


    panels = [
        ImageChooserPanel('banner_background'),
        ImageChooserPanel('logo_slide'),
        ImageChooserPanel('logo'),
        ImageChooserPanel('profile_pic'),
        ImageChooserPanel('image'),
        ImageChooserPanel('image_2'),
        ImageChooserPanel('image_3'),
        ImageChooserPanel('image_4'),
        ImageChooserPanel('image_1'),
        ImageChooserPanel('image_2_2'),
        ImageChooserPanel('image_3_3'),
        ImageChooserPanel('image_4_4'),
    ]

@register_setting
class SocialMediaSettings(BaseSetting):
    facebook = models.URLField(blank=True,null=True,help_text="")
    twitter = models.URLField(blank=True,null=True,help_text="")
    instagram = models.URLField(blank=True,null=True,help_text="")
    youtube = models.URLField(blank=True,null=True,help_text="")
   # behance = models.URLField(blank=True,null=True,help_text="")
    linkedin = models.URLField(blank=True,null=True,help_text="")

    panels = [
        MultiFieldPanel(
            [
            FieldPanel("facebook"),
            FieldPanel("twitter"),
            FieldPanel("instagram"),
            FieldPanel("youtube"),  
         #   FieldPanel("behance"),
            FieldPanel("linkedin"),         
            ]
        ,heading= "Social Media Settings")
    ]

@register_setting
class GlobalLinksSettings(BaseSetting):
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



    # pagina de Contactos
class consultascontact(AbstractFormField):
    page = ParentalKey('contactus', on_delete=models.CASCADE, related_name='form_fields')
class contactus(AbstractEmailForm):
    # Empieza Barner de Inicio
    template = "webapp/home/contactus.html"
    #cliente_Navbar = RichTextField(blank=True,verbose_name='Cliente-url')
    
   # banner_title1 = RichTextField(blank=True,verbose_name='Titulo del primer banner ')
   # banner_info1 = RichTextField(blank=True,verbose_name='Informacion del primer banner ')
   # banner_title2 = RichTextField(blank=True,verbose_name='Titulo del segundo banner ')
   # banner_info2 = RichTextField(blank=True,verbose_name='Informacion del segundo banner ')
   # banner_title3 = RichTextField(blank=True,verbose_name='Titulo del tercer banner ')
   # banner_info3 = RichTextField(blank=True,verbose_name='Informacion del tercer banner ')

    # Empieza Banner de sliders
    bio = RichTextField(blank=True,verbose_name='rseña bibliografica')

    banner_title4 = RichTextField(blank=True,verbose_name='Titulo de galeria-1 ')
    TS_info1 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Subtitulo info')
    info1 = models.CharField(max_length=150, null=True, blank=True,verbose_name='info')
    banner_title5 = RichTextField(blank=True,verbose_name='Titulo de galeria-2  ')
    TS_info2 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Subtitulo-2 info')
    info2 = models.CharField(max_length=150, null=True, blank=True,verbose_name='info-2')
    banner_title6 = RichTextField(blank=True,verbose_name='Titulo de galeria-3  ')
    TS_info3 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Subtitulo-3 info')
    info3 = models.CharField(max_length=150, null=True, blank=True,verbose_name='info-3')
    banner_title7 = RichTextField(blank=True,verbose_name='Titulo de galeria-4  ')
    TS_info4 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Subtitulot-4 info')
    info4 = models.CharField(max_length=150, null=True, blank=True,verbose_name='info-4')
    banner_title8 = RichTextField(blank=True,verbose_name='Titulo de galeria-5  ')
    TS_info5 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Subtitulo-5 info')
    info5 = models.CharField(max_length=150, null=True, blank=True,verbose_name='info-5')
    banner_title9 = RichTextField(blank=True,verbose_name='Titulo de galeria-6  ')
    TS_info6 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Subtitulo-6 info')
    info6 = models.CharField(max_length=150, null=True, blank=True,verbose_name='info-6')


    # Empieza Banner de callout
    banner_title10 = RichTextField(blank=True,verbose_name='we improve')
    info7 = models.CharField(max_length=150, null=True, blank=True,verbose_name='IT business analytics')
    info8 = models.CharField(max_length=150, null=True, blank=True,verbose_name='IT business cloud DevOps')
    info9 = models.CharField(max_length=150, null=True, blank=True,verbose_name='IT business Media')
    
    # Empieza Banner de Products

  
    product_1 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Product-1')
    product_description_1 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Descripcion Product-1')
    product_2 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Product-2')
    product_description_2 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Descripcion Product-2')
    product_3 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Product-3')
    product_description_3 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Descripcion Product-3')
    product_4 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Product-4')
    product_description_4 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Descripcion Product-4')
    product_5 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Product-5')
    product_description_5 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Descripcion Product-5')
    product_6 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Product-6')
    product_description_6 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Descripcion Product-6')
    # Banner contador
    numero_coffe = models.IntegerField( null=True)
    numero_experiencia =  models.IntegerField( null=True)
    numero_horas = models.IntegerField( null=True)
    numero_wins = models.IntegerField(null=True)


    team_1 = models.CharField(max_length=150, null=True, blank=True,verbose_name='team-1')
    team_descrp_1 = models.CharField(max_length=150, null=True, blank=True,verbose_name='team descripcion-1')
    team_2 = models.CharField(max_length=150, null=True, blank=True,verbose_name='team-2')
    team_descrp_2 = models.CharField(max_length=150, null=True, blank=True,verbose_name='team descripcion-2')
    team_3 = models.CharField(max_length=150, null=True, blank=True,verbose_name='team-3')
    team_descrp_3 = models.CharField(max_length=150, null=True, blank=True,verbose_name='team descripcion-3')
    team_4 = models.CharField(max_length=150, null=True, blank=True,verbose_name='team-4')
    team_descrp_4 = models.CharField(max_length=150, null=True, blank=True,verbose_name='team descripcion-4')

    banner_title = models.CharField(max_length=150, null=True, blank=True,verbose_name='Call Action Title')
    slogan = models.CharField(max_length=150, null=True, blank=True,verbose_name='slogan')
    slogan_descriptcion = models.CharField(max_length=150, null=True, blank=True,verbose_name='slogan Description')
    


    custom_title = models.CharField(max_length=100,blank=True,null=True,help_text="Reescribe el  Titulo de la publicacion ")


    
    # Campos de consulta

    consulta= RichTextField(blank=True,verbose_name='Mensaje para que nos consulten por el formulario')
    thank_you_text = RichTextField(blank=True)
    # galeria de imagenes barner de presentacion

    content_panels = AbstractEmailForm.content_panels + Page.content_panels + [


    #Panel sliders
        FieldPanel('bio', classname="full"),
        FieldPanel('banner_title4', classname="full"),
        FieldPanel('TS_info1', classname="full"),
        FieldPanel('info1', classname="full"),
        FieldPanel('banner_title5', classname="full"),
        FieldPanel('TS_info2', classname="full"),
        FieldPanel('info2', classname="full"),
        FieldPanel('banner_title6', classname="full"),
        FieldPanel('TS_info3', classname="full"),
        FieldPanel('info3', classname="full"),
        FieldPanel('banner_title7', classname="full"),
        FieldPanel('TS_info4', classname="full"),
        FieldPanel('info4', classname="full"),
        FieldPanel('banner_title8', classname="full"),
        FieldPanel('TS_info5', classname="full"),
        FieldPanel('info5', classname="full"),
        FieldPanel('banner_title9', classname="full"),
        FieldPanel('TS_info6', classname="full"),
        FieldPanel('info6', classname="full"),
        FieldPanel('banner_title10', classname="full"),
        FieldPanel('info7', classname="full"),
        FieldPanel('info8', classname="full"),
        FieldPanel('info9', classname="full"),


        FieldPanel('product_1', classname="full"),
        FieldPanel('product_description_1', classname="full"),
        FieldPanel('product_2', classname="full"),
        FieldPanel('product_description_2', classname="full"),
        FieldPanel('product_3', classname="full"),
        FieldPanel('product_description_3', classname="full"),
        FieldPanel('product_4', classname="full"),
        FieldPanel('product_description_4', classname="full"),
        FieldPanel('product_5', classname="full"),
        FieldPanel('product_description_5', classname="full"),
        FieldPanel('product_6', classname="full"),
        FieldPanel('product_description_6', classname="full"),
        FieldPanel('numero_coffe', classname="full"),
        FieldPanel('numero_experiencia', classname="full"),
        FieldPanel('numero_horas', classname="full"),
        FieldPanel('numero_wins', classname="full"),
        FieldPanel('team_1', classname="full"),
        FieldPanel('team_descrp_1', classname="full"),
        FieldPanel('team_2', classname="full"),
        FieldPanel('team_descrp_2', classname="full"),
        FieldPanel('team_3', classname="full"),
        FieldPanel('team_descrp_3', classname="full"),
        FieldPanel('team_4', classname="full"),
        FieldPanel('team_descrp_4', classname="full"),
        FieldPanel('banner_title', classname="full"),
        FieldPanel('slogan', classname="full"),
        FieldPanel('slogan_descriptcion', classname="full"),


#panel 
        FieldPanel('consulta', classname="full"),

        InlinePanel('galleria_contacus', label="Imagen de Fondo Barner"),
        FormSubmissionsPanel(),
        InlinePanel('form_fields', label="consultashome"),
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
class GaleriaContactus(Orderable):
    page = ParentalKey(contactus, on_delete=models.CASCADE, related_name='galleria_contacus')
    logo = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Logotipo SmartQuail')
    profile_pic = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto de perfil')
    image = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 1')
    image_2 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 2')
    image_3 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 3')
    image_4 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 4')
    image_5 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 5')
    image_6 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 6')
    image_7 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen product 1')
    image_8 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen product 2')
    image_9 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen product 3')
    image_10 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen product 4')
    image_11 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen product 5')
    image_12 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen product 6')
    image_13 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen team 1')
    image_14 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen team 2')
    image_15 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen team 3')
    image_16 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen team 4')
    image_17 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='logo_parther')
    image_18 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='logo_parther')
    image_19 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='logo_parther')
    image_20 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='logo_parther')
    image_21 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='logo_parther')
    image_22 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='logo_parther')
    image_23 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='logo_parther')
    image_24 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='logo_parther')
    image_25 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='logo_parther')
    image_26 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='logo_parther')

    panels = [
        ImageChooserPanel('logo'),
        ImageChooserPanel('profile_pic'),
        ImageChooserPanel('image'),
        ImageChooserPanel('image_2'),
        ImageChooserPanel('image_3'),
        ImageChooserPanel('image_4'),
        ImageChooserPanel('image_5'),
        ImageChooserPanel('image_6'),
        ImageChooserPanel('image_7'),
        ImageChooserPanel('image_8'),
        ImageChooserPanel('image_9'),
        ImageChooserPanel('image_10'),
        ImageChooserPanel('image_11'),
        ImageChooserPanel('image_12'),
        ImageChooserPanel('image_13'),
        ImageChooserPanel('image_14'),
        ImageChooserPanel('image_15'),
        ImageChooserPanel('image_16'),
        ImageChooserPanel('image_17'),
        ImageChooserPanel('image_18'),
        ImageChooserPanel('image_19'),
        ImageChooserPanel('image_20'),
        ImageChooserPanel('image_21'),
        ImageChooserPanel('image_22'),
        ImageChooserPanel('image_23'),
        ImageChooserPanel('image_24'),
        ImageChooserPanel('image_25'),
        ImageChooserPanel('image_26'),
    ]

# Pagina para datos de clientes 
class consultascreateitbusiness(AbstractFormField):
    page = ParentalKey('createitbusiness', on_delete=models.CASCADE, related_name='form_fields')
class createitbusiness(AbstractEmailForm):
    # Empieza Barner de Inicio
    template = "webapp/createitbusiness/createitbusiness.html"
    #cliente_Navbar = RichTextField(blank=True,verbose_name='Cliente-url')
    
   # banner_title1 = RichTextField(blank=True,verbose_name='Titulo del primer banner ')
   # banner_info1 = RichTextField(blank=True,verbose_name='Informacion del primer banner ')
   # banner_title2 = RichTextField(blank=True,verbose_name='Titulo del segundo banner ')
   # banner_info2 = RichTextField(blank=True,verbose_name='Informacion del segundo banner ')
   # banner_title3 = RichTextField(blank=True,verbose_name='Titulo del tercer banner ')
   # banner_info3 = RichTextField(blank=True,verbose_name='Informacion del tercer banner ')

    # Empieza Banner de sliders
    bio = RichTextField(blank=True,verbose_name='rseña bibliografica')

    banner_title4 = RichTextField(blank=True,verbose_name='Titulo de galeria-1 ')
    TS_info1 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Subtitulo info')
    info1 = models.CharField(max_length=150, null=True, blank=True,verbose_name='info')
    banner_title5 = RichTextField(blank=True,verbose_name='Titulo de galeria-2  ')
    TS_info2 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Subtitulo-2 info')
    info2 = models.CharField(max_length=150, null=True, blank=True,verbose_name='info-2')
    banner_title6 = RichTextField(blank=True,verbose_name='Titulo de galeria-3  ')
    TS_info3 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Subtitulo-3 info')
    info3 = models.CharField(max_length=150, null=True, blank=True,verbose_name='info-3')
    banner_title7 = RichTextField(blank=True,verbose_name='Titulo de galeria-4  ')
    TS_info4 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Subtitulot-4 info')
    info4 = models.CharField(max_length=150, null=True, blank=True,verbose_name='info-4')
    banner_title8 = RichTextField(blank=True,verbose_name='Titulo de galeria-5  ')
    TS_info5 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Subtitulo-5 info')
    info5 = models.CharField(max_length=150, null=True, blank=True,verbose_name='info-5')
    banner_title9 = RichTextField(blank=True,verbose_name='Titulo de galeria-6  ')
    TS_info6 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Subtitulo-6 info')
    info6 = models.CharField(max_length=150, null=True, blank=True,verbose_name='info-6')


    # Empieza Banner de callout
    banner_title10 = RichTextField(blank=True,verbose_name='we improve')
    info7 = models.CharField(max_length=150, null=True, blank=True,verbose_name='IT business analytics')
    info8 = models.CharField(max_length=150, null=True, blank=True,verbose_name='IT business cloud DevOps')
    info9 = models.CharField(max_length=150, null=True, blank=True,verbose_name='IT business Media')
    
    # Empieza Banner de Products

  
    product_1 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Product-1')
    product_description_1 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Descripcion Product-1')
    product_2 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Product-2')
    product_description_2 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Descripcion Product-2')
    product_3 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Product-3')
    product_description_3 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Descripcion Product-3')
    product_4 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Product-4')
    product_description_4 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Descripcion Product-4')
    product_5 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Product-5')
    product_description_5 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Descripcion Product-5')
    product_6 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Product-6')
    product_description_6 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Descripcion Product-6')
    # Banner contador
    numero_coffe = models.IntegerField( null=True)
    numero_experiencia =  models.IntegerField( null=True)
    numero_horas = models.IntegerField( null=True)
    numero_wins = models.IntegerField(null=True)


    team_1 = models.CharField(max_length=150, null=True, blank=True,verbose_name='team-1')
    team_descrp_1 = models.CharField(max_length=150, null=True, blank=True,verbose_name='team descripcion-1')
    team_2 = models.CharField(max_length=150, null=True, blank=True,verbose_name='team-2')
    team_descrp_2 = models.CharField(max_length=150, null=True, blank=True,verbose_name='team descripcion-2')
    team_3 = models.CharField(max_length=150, null=True, blank=True,verbose_name='team-3')
    team_descrp_3 = models.CharField(max_length=150, null=True, blank=True,verbose_name='team descripcion-3')
    team_4 = models.CharField(max_length=150, null=True, blank=True,verbose_name='team-4')
    team_descrp_4 = models.CharField(max_length=150, null=True, blank=True,verbose_name='team descripcion-4')

    banner_title = models.CharField(max_length=150, null=True, blank=True,verbose_name='Call Action Title')
    slogan = models.CharField(max_length=150, null=True, blank=True,verbose_name='slogan')
    slogan_descriptcion = models.CharField(max_length=150, null=True, blank=True,verbose_name='slogan Description')
    


    custom_title = models.CharField(max_length=100,blank=True,null=True,help_text="Reescribe el  Titulo de la publicacion ")


    
    # Campos de consulta

    consulta= RichTextField(blank=True,verbose_name='Mensaje para que nos consulten por el formulario')
    thank_you_text = RichTextField(blank=True)
    # galeria de imagenes barner de presentacion

    content_panels = AbstractEmailForm.content_panels + Page.content_panels + [


    #Panel sliders
        FieldPanel('bio', classname="full"),
        FieldPanel('banner_title4', classname="full"),
        FieldPanel('TS_info1', classname="full"),
        FieldPanel('info1', classname="full"),
        FieldPanel('banner_title5', classname="full"),
        FieldPanel('TS_info2', classname="full"),
        FieldPanel('info2', classname="full"),
        FieldPanel('banner_title6', classname="full"),
        FieldPanel('TS_info3', classname="full"),
        FieldPanel('info3', classname="full"),
        FieldPanel('banner_title7', classname="full"),
        FieldPanel('TS_info4', classname="full"),
        FieldPanel('info4', classname="full"),
        FieldPanel('banner_title8', classname="full"),
        FieldPanel('TS_info5', classname="full"),
        FieldPanel('info5', classname="full"),
        FieldPanel('banner_title9', classname="full"),
        FieldPanel('TS_info6', classname="full"),
        FieldPanel('info6', classname="full"),
        FieldPanel('banner_title10', classname="full"),
        FieldPanel('info7', classname="full"),
        FieldPanel('info8', classname="full"),
        FieldPanel('info9', classname="full"),


        FieldPanel('product_1', classname="full"),
        FieldPanel('product_description_1', classname="full"),
        FieldPanel('product_2', classname="full"),
        FieldPanel('product_description_2', classname="full"),
        FieldPanel('product_3', classname="full"),
        FieldPanel('product_description_3', classname="full"),
        FieldPanel('product_4', classname="full"),
        FieldPanel('product_description_4', classname="full"),
        FieldPanel('product_5', classname="full"),
        FieldPanel('product_description_5', classname="full"),
        FieldPanel('product_6', classname="full"),
        FieldPanel('product_description_6', classname="full"),
        FieldPanel('numero_coffe', classname="full"),
        FieldPanel('numero_experiencia', classname="full"),
        FieldPanel('numero_horas', classname="full"),
        FieldPanel('numero_wins', classname="full"),
        FieldPanel('team_1', classname="full"),
        FieldPanel('team_descrp_1', classname="full"),
        FieldPanel('team_2', classname="full"),
        FieldPanel('team_descrp_2', classname="full"),
        FieldPanel('team_3', classname="full"),
        FieldPanel('team_descrp_3', classname="full"),
        FieldPanel('team_4', classname="full"),
        FieldPanel('team_descrp_4', classname="full"),
        FieldPanel('banner_title', classname="full"),
        FieldPanel('slogan', classname="full"),
        FieldPanel('slogan_descriptcion', classname="full"),


#panel 
        FieldPanel('consulta', classname="full"),

        InlinePanel('galleria_contacus', label="Imagen de Fondo Barner"),
        FormSubmissionsPanel(),
        InlinePanel('form_fields', label="consultashome"),
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
class Galeriacreateitbusiness(Orderable):
    page = ParentalKey(createitbusiness, on_delete=models.CASCADE, related_name='galleria_contacus')
    logo = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Logotipo SmartQuail')
    profile_pic = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto de perfil')
    image = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 1')
    image_2 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 2')
    image_3 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 3')
    image_4 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 4')
    image_5 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 5')
    image_6 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 6')
    image_7 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen product 1')
    image_8 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen product 2')
    image_9 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen product 3')
    image_10 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen product 4')
    image_11 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen product 5')
    image_12 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen product 6')
    image_13 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen team 1')
    image_14 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen team 2')
    image_15 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen team 3')
    image_16 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen team 4')
    image_17 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='logo_parther')
    image_18 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='logo_parther')
    image_19 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='logo_parther')
    image_20 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='logo_parther')
    image_21 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='logo_parther')
    image_22 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='logo_parther')
    image_23 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='logo_parther')
    image_24 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='logo_parther')
    image_25 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='logo_parther')
    image_26 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='logo_parther')

    panels = [
        ImageChooserPanel('logo'),
        ImageChooserPanel('profile_pic'),
        ImageChooserPanel('image'),
        ImageChooserPanel('image_2'),
        ImageChooserPanel('image_3'),
        ImageChooserPanel('image_4'),
        ImageChooserPanel('image_5'),
        ImageChooserPanel('image_6'),
        ImageChooserPanel('image_7'),
        ImageChooserPanel('image_8'),
        ImageChooserPanel('image_9'),
        ImageChooserPanel('image_10'),
        ImageChooserPanel('image_11'),
        ImageChooserPanel('image_12'),
        ImageChooserPanel('image_13'),
        ImageChooserPanel('image_14'),
        ImageChooserPanel('image_15'),
        ImageChooserPanel('image_16'),
        ImageChooserPanel('image_17'),
        ImageChooserPanel('image_18'),
        ImageChooserPanel('image_19'),
        ImageChooserPanel('image_20'),
        ImageChooserPanel('image_21'),
        ImageChooserPanel('image_22'),
        ImageChooserPanel('image_23'),
        ImageChooserPanel('image_24'),
        ImageChooserPanel('image_25'),
        ImageChooserPanel('image_26'),
    ]


# Pagina para datos de clientes 
class consultascreateprojects(AbstractFormField):
    page = ParentalKey('createprojects', on_delete=models.CASCADE, related_name='form_fields')
class createprojects(AbstractEmailForm):
    # Empieza Barner de Inicio
    template = "webapp/createitbusiness/createprojects.html"
    #cliente_Navbar = RichTextField(blank=True,verbose_name='Cliente-url')
    
   # banner_title1 = RichTextField(blank=True,verbose_name='Titulo del primer banner ')
   # banner_info1 = RichTextField(blank=True,verbose_name='Informacion del primer banner ')
   # banner_title2 = RichTextField(blank=True,verbose_name='Titulo del segundo banner ')
   # banner_info2 = RichTextField(blank=True,verbose_name='Informacion del segundo banner ')
   # banner_title3 = RichTextField(blank=True,verbose_name='Titulo del tercer banner ')
   # banner_info3 = RichTextField(blank=True,verbose_name='Informacion del tercer banner ')

    # Empieza Banner de sliders
    bio = RichTextField(blank=True,verbose_name='rseña bibliografica')

    banner_title4 = RichTextField(blank=True,verbose_name='Titulo de galeria-1 ')
    TS_info1 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Subtitulo info')
    info1 = models.CharField(max_length=150, null=True, blank=True,verbose_name='info')
    banner_title5 = RichTextField(blank=True,verbose_name='Titulo de galeria-2  ')
    TS_info2 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Subtitulo-2 info')
    info2 = models.CharField(max_length=150, null=True, blank=True,verbose_name='info-2')
    banner_title6 = RichTextField(blank=True,verbose_name='Titulo de galeria-3  ')
    TS_info3 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Subtitulo-3 info')
    info3 = models.CharField(max_length=150, null=True, blank=True,verbose_name='info-3')
    banner_title7 = RichTextField(blank=True,verbose_name='Titulo de galeria-4  ')
    TS_info4 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Subtitulot-4 info')
    info4 = models.CharField(max_length=150, null=True, blank=True,verbose_name='info-4')
    banner_title8 = RichTextField(blank=True,verbose_name='Titulo de galeria-5  ')
    TS_info5 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Subtitulo-5 info')
    info5 = models.CharField(max_length=150, null=True, blank=True,verbose_name='info-5')
    banner_title9 = RichTextField(blank=True,verbose_name='Titulo de galeria-6  ')
    TS_info6 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Subtitulo-6 info')
    info6 = models.CharField(max_length=150, null=True, blank=True,verbose_name='info-6')


    # Empieza Banner de callout
    banner_title10 = RichTextField(blank=True,verbose_name='we improve')
    info7 = models.CharField(max_length=150, null=True, blank=True,verbose_name='IT business analytics')
    info8 = models.CharField(max_length=150, null=True, blank=True,verbose_name='IT business cloud DevOps')
    info9 = models.CharField(max_length=150, null=True, blank=True,verbose_name='IT business Media')
    
    # Empieza Banner de Products

  
    product_1 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Product-1')
    product_description_1 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Descripcion Product-1')
    product_2 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Product-2')
    product_description_2 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Descripcion Product-2')
    product_3 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Product-3')
    product_description_3 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Descripcion Product-3')
    product_4 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Product-4')
    product_description_4 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Descripcion Product-4')
    product_5 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Product-5')
    product_description_5 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Descripcion Product-5')
    product_6 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Product-6')
    product_description_6 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Descripcion Product-6')
    # Banner contador
    numero_coffe = models.IntegerField( null=True)
    numero_experiencia =  models.IntegerField( null=True)
    numero_horas = models.IntegerField( null=True)
    numero_wins = models.IntegerField(null=True)


    team_1 = models.CharField(max_length=150, null=True, blank=True,verbose_name='team-1')
    team_descrp_1 = models.CharField(max_length=150, null=True, blank=True,verbose_name='team descripcion-1')
    team_2 = models.CharField(max_length=150, null=True, blank=True,verbose_name='team-2')
    team_descrp_2 = models.CharField(max_length=150, null=True, blank=True,verbose_name='team descripcion-2')
    team_3 = models.CharField(max_length=150, null=True, blank=True,verbose_name='team-3')
    team_descrp_3 = models.CharField(max_length=150, null=True, blank=True,verbose_name='team descripcion-3')
    team_4 = models.CharField(max_length=150, null=True, blank=True,verbose_name='team-4')
    team_descrp_4 = models.CharField(max_length=150, null=True, blank=True,verbose_name='team descripcion-4')

    banner_title = models.CharField(max_length=150, null=True, blank=True,verbose_name='Call Action Title')
    slogan = models.CharField(max_length=150, null=True, blank=True,verbose_name='slogan')
    slogan_descriptcion = models.CharField(max_length=150, null=True, blank=True,verbose_name='slogan Description')
    


    custom_title = models.CharField(max_length=100,blank=True,null=True,help_text="Reescribe el  Titulo de la publicacion ")


    
    # Campos de consulta

    consulta= RichTextField(blank=True,verbose_name='Mensaje para que nos consulten por el formulario')
    thank_you_text = RichTextField(blank=True)
    # galeria de imagenes barner de presentacion

    content_panels = AbstractEmailForm.content_panels + Page.content_panels + [


    #Panel sliders
        FieldPanel('bio', classname="full"),
        FieldPanel('banner_title4', classname="full"),
        FieldPanel('TS_info1', classname="full"),
        FieldPanel('info1', classname="full"),
        FieldPanel('banner_title5', classname="full"),
        FieldPanel('TS_info2', classname="full"),
        FieldPanel('info2', classname="full"),
        FieldPanel('banner_title6', classname="full"),
        FieldPanel('TS_info3', classname="full"),
        FieldPanel('info3', classname="full"),
        FieldPanel('banner_title7', classname="full"),
        FieldPanel('TS_info4', classname="full"),
        FieldPanel('info4', classname="full"),
        FieldPanel('banner_title8', classname="full"),
        FieldPanel('TS_info5', classname="full"),
        FieldPanel('info5', classname="full"),
        FieldPanel('banner_title9', classname="full"),
        FieldPanel('TS_info6', classname="full"),
        FieldPanel('info6', classname="full"),
        FieldPanel('banner_title10', classname="full"),
        FieldPanel('info7', classname="full"),
        FieldPanel('info8', classname="full"),
        FieldPanel('info9', classname="full"),


        FieldPanel('product_1', classname="full"),
        FieldPanel('product_description_1', classname="full"),
        FieldPanel('product_2', classname="full"),
        FieldPanel('product_description_2', classname="full"),
        FieldPanel('product_3', classname="full"),
        FieldPanel('product_description_3', classname="full"),
        FieldPanel('product_4', classname="full"),
        FieldPanel('product_description_4', classname="full"),
        FieldPanel('product_5', classname="full"),
        FieldPanel('product_description_5', classname="full"),
        FieldPanel('product_6', classname="full"),
        FieldPanel('product_description_6', classname="full"),
        FieldPanel('numero_coffe', classname="full"),
        FieldPanel('numero_experiencia', classname="full"),
        FieldPanel('numero_horas', classname="full"),
        FieldPanel('numero_wins', classname="full"),
        FieldPanel('team_1', classname="full"),
        FieldPanel('team_descrp_1', classname="full"),
        FieldPanel('team_2', classname="full"),
        FieldPanel('team_descrp_2', classname="full"),
        FieldPanel('team_3', classname="full"),
        FieldPanel('team_descrp_3', classname="full"),
        FieldPanel('team_4', classname="full"),
        FieldPanel('team_descrp_4', classname="full"),
        FieldPanel('banner_title', classname="full"),
        FieldPanel('slogan', classname="full"),
        FieldPanel('slogan_descriptcion', classname="full"),


#panel 
        FieldPanel('consulta', classname="full"),

        InlinePanel('galleria_contacus', label="Imagen de Fondo Barner"),
        FormSubmissionsPanel(),
        InlinePanel('form_fields', label="consultashome"),
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
class Galeriacreateprojects(Orderable):
    page = ParentalKey(createprojects, on_delete=models.CASCADE, related_name='galleria_contacus')
    logo = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Logotipo SmartQuail')
    profile_pic = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto de perfil')
    image = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 1')
    image_2 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 2')
    image_3 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 3')
    image_4 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 4')
    image_5 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 5')
    image_6 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 6')
    image_7 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen product 1')
    image_8 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen product 2')
    image_9 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen product 3')
    image_10 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen product 4')
    image_11 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen product 5')
    image_12 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen product 6')
    image_13 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen team 1')
    image_14 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen team 2')
    image_15 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen team 3')
    image_16 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen team 4')
    image_17 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='logo_parther')
    image_18 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='logo_parther')
    image_19 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='logo_parther')
    image_20 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='logo_parther')
    image_21 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='logo_parther')
    image_22 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='logo_parther')
    image_23 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='logo_parther')
    image_24 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='logo_parther')
    image_25 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='logo_parther')
    image_26 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='logo_parther')

    panels = [
        ImageChooserPanel('logo'),
        ImageChooserPanel('profile_pic'),
        ImageChooserPanel('image'),
        ImageChooserPanel('image_2'),
        ImageChooserPanel('image_3'),
        ImageChooserPanel('image_4'),
        ImageChooserPanel('image_5'),
        ImageChooserPanel('image_6'),
        ImageChooserPanel('image_7'),
        ImageChooserPanel('image_8'),
        ImageChooserPanel('image_9'),
        ImageChooserPanel('image_10'),
        ImageChooserPanel('image_11'),
        ImageChooserPanel('image_12'),
        ImageChooserPanel('image_13'),
        ImageChooserPanel('image_14'),
        ImageChooserPanel('image_15'),
        ImageChooserPanel('image_16'),
        ImageChooserPanel('image_17'),
        ImageChooserPanel('image_18'),
        ImageChooserPanel('image_19'),
        ImageChooserPanel('image_20'),
        ImageChooserPanel('image_21'),
        ImageChooserPanel('image_22'),
        ImageChooserPanel('image_23'),
        ImageChooserPanel('image_24'),
        ImageChooserPanel('image_25'),
        ImageChooserPanel('image_26'),
    ]

class solutions_categories(Page):
    solution_name = models.CharField(max_length=150, null=True, blank=True,verbose_name='Solution Name')
    solution_category = models.CharField(max_length=150, null=True, blank=True,verbose_name='Solution Category')
    date = models.DateField("Post date",null= True)

    content_panels = Page.content_panels + [
        FieldPanel('date', classname="full"),
        FieldPanel('solution_name', classname="full"),
        FieldPanel('solution_category', classname="full"),
    ]


# Pagina para datos de clientes 
class consultassolutions(AbstractFormField):
    page = ParentalKey('solutions', on_delete=models.CASCADE, related_name='form_fields')
class solutions(AbstractEmailForm):
    # Empieza Barner de Inicio
    template = "webapp/solutions/solutions.html"

    #cliente_Navbar = RichTextField(blank=True,verbose_name='Cliente-url')
    
   # banner_title1 = RichTextField(blank=True,verbose_name='Titulo del primer banner ')
   # banner_info1 = RichTextField(blank=True,verbose_name='Informacion del primer banner ')
   # banner_title2 = RichTextField(blank=True,verbose_name='Titulo del segundo banner ')
   # banner_info2 = RichTextField(blank=True,verbose_name='Informacion del segundo banner ')
   # banner_title3 = RichTextField(blank=True,verbose_name='Titulo del tercer banner ')
   # banner_info3 = RichTextField(blank=True,verbose_name='Informacion del tercer banner ')

    # Empieza Banner de sliders
    bio = RichTextField(blank=True,verbose_name='rseña bibliografica')
    #Blog app

    category = models.ForeignKey(solutions_categories, related_name='items',on_delete=models.CASCADE, null= True)

    TS_info1 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Subtitulo info')
    info1 = models.CharField(max_length=150, null=True, blank=True,verbose_name='info')
    banner_title5 = RichTextField(blank=True,verbose_name='Titulo de galeria-2  ')
    TS_info2 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Subtitulo-2 info')
    info2 = models.CharField(max_length=150, null=True, blank=True,verbose_name='info-2')
    banner_title6 = RichTextField(blank=True,verbose_name='Titulo de galeria-3  ')
    TS_info3 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Subtitulo-3 info')
    info3 = models.CharField(max_length=150, null=True, blank=True,verbose_name='info-3')
    banner_title7 = RichTextField(blank=True,verbose_name='Titulo de galeria-4  ')
    TS_info4 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Subtitulot-4 info')
    info4 = models.CharField(max_length=150, null=True, blank=True,verbose_name='info-4')
    banner_title8 = RichTextField(blank=True,verbose_name='Titulo de galeria-5  ')
    TS_info5 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Subtitulo-5 info')
    info5 = models.CharField(max_length=150, null=True, blank=True,verbose_name='info-5')
    banner_title9 = RichTextField(blank=True,verbose_name='Titulo de galeria-6  ')
    TS_info6 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Subtitulo-6 info')
    info6 = models.CharField(max_length=150, null=True, blank=True,verbose_name='info-6')


    # Empieza Banner de callout
    banner_title10 = RichTextField(blank=True,verbose_name='we improve')
    info7 = models.CharField(max_length=150, null=True, blank=True,verbose_name='IT business analytics')
    info8 = models.CharField(max_length=150, null=True, blank=True,verbose_name='IT business cloud DevOps')
    info9 = models.CharField(max_length=150, null=True, blank=True,verbose_name='IT business Media')
    
    # Empieza Banner de Products

  
    product_1 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Product-1')
    product_description_1 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Descripcion Product-1')
    product_2 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Product-2')
    product_description_2 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Descripcion Product-2')
    product_3 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Product-3')
    product_description_3 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Descripcion Product-3')
    product_4 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Product-4')
    product_description_4 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Descripcion Product-4')
    product_5 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Product-5')
    product_description_5 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Descripcion Product-5')
    product_6 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Product-6')
    product_description_6 = models.CharField(max_length=150, null=True, blank=True,verbose_name='Descripcion Product-6')
    # Banner contador
    numero_coffe = models.IntegerField( null=True)
    numero_experiencia =  models.IntegerField( null=True)
    numero_horas = models.IntegerField( null=True)
    numero_wins = models.IntegerField(null=True)


    team_1 = models.CharField(max_length=150, null=True, blank=True,verbose_name='team-1')
    team_descrp_1 = models.CharField(max_length=150, null=True, blank=True,verbose_name='team descripcion-1')
    team_2 = models.CharField(max_length=150, null=True, blank=True,verbose_name='team-2')
    team_descrp_2 = models.CharField(max_length=150, null=True, blank=True,verbose_name='team descripcion-2')
    team_3 = models.CharField(max_length=150, null=True, blank=True,verbose_name='team-3')
    team_descrp_3 = models.CharField(max_length=150, null=True, blank=True,verbose_name='team descripcion-3')
    team_4 = models.CharField(max_length=150, null=True, blank=True,verbose_name='team-4')
    team_descrp_4 = models.CharField(max_length=150, null=True, blank=True,verbose_name='team descripcion-4')

    banner_title = models.CharField(max_length=150, null=True, blank=True,verbose_name='Call Action Title')
    slogan = models.CharField(max_length=150, null=True, blank=True,verbose_name='slogan')
    slogan_descriptcion = models.CharField(max_length=150, null=True, blank=True,verbose_name='slogan Description')
    


    custom_title = models.CharField(max_length=100,blank=True,null=True,help_text="Reescribe el  Titulo de la publicacion ")


    
    # Campos de consulta

    consulta= RichTextField(blank=True,verbose_name='Mensaje para que nos consulten por el formulario')
    thank_you_text = RichTextField(blank=True)
    # galeria de imagenes barner de presentacion

    content_panels = AbstractEmailForm.content_panels + Page.content_panels + [


    #Panel sliders
        FieldPanel('bio', classname="full"),
        
        FieldPanel('category', classname="full"),
        FieldPanel('TS_info1', classname="full"),
        FieldPanel('info1', classname="full"),
        FieldPanel('banner_title5', classname="full"),
        FieldPanel('TS_info2', classname="full"),
        FieldPanel('info2', classname="full"),
        FieldPanel('banner_title6', classname="full"),
        FieldPanel('TS_info3', classname="full"),
        FieldPanel('info3', classname="full"),
        FieldPanel('banner_title7', classname="full"),
        FieldPanel('TS_info4', classname="full"),
        FieldPanel('info4', classname="full"),
        FieldPanel('banner_title8', classname="full"),
        FieldPanel('TS_info5', classname="full"),
        FieldPanel('info5', classname="full"),
        FieldPanel('banner_title9', classname="full"),
        FieldPanel('TS_info6', classname="full"),
        FieldPanel('info6', classname="full"),
        FieldPanel('banner_title10', classname="full"),
        FieldPanel('info7', classname="full"),
        FieldPanel('info8', classname="full"),
        FieldPanel('info9', classname="full"),


        FieldPanel('product_1', classname="full"),
        FieldPanel('product_description_1', classname="full"),
        FieldPanel('product_2', classname="full"),
        FieldPanel('product_description_2', classname="full"),
        FieldPanel('product_3', classname="full"),
        FieldPanel('product_description_3', classname="full"),
        FieldPanel('product_4', classname="full"),
        FieldPanel('product_description_4', classname="full"),
        FieldPanel('product_5', classname="full"),
        FieldPanel('product_description_5', classname="full"),
        FieldPanel('product_6', classname="full"),
        FieldPanel('product_description_6', classname="full"),
        FieldPanel('numero_coffe', classname="full"),
        FieldPanel('numero_experiencia', classname="full"),
        FieldPanel('numero_horas', classname="full"),
        FieldPanel('numero_wins', classname="full"),
        FieldPanel('team_1', classname="full"),
        FieldPanel('team_descrp_1', classname="full"),
        FieldPanel('team_2', classname="full"),
        FieldPanel('team_descrp_2', classname="full"),
        FieldPanel('team_3', classname="full"),
        FieldPanel('team_descrp_3', classname="full"),
        FieldPanel('team_4', classname="full"),
        FieldPanel('team_descrp_4', classname="full"),
        FieldPanel('banner_title', classname="full"),
        FieldPanel('slogan', classname="full"),
        FieldPanel('slogan_descriptcion', classname="full"),


#panel 
        FieldPanel('consulta', classname="full"),

        InlinePanel('galleria_contacus', label="Imagen de Fondo Barner"),
        FormSubmissionsPanel(),
        InlinePanel('form_fields', label="consultashome"),
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
class Galeriacreatesolutions(Orderable):
    page = ParentalKey(solutions, on_delete=models.CASCADE, related_name='galleria_contacus')
    logo = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Logotipo SmartQuail')
    profile_pic = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto de perfil')
    image = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 1')
    image_2 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 2')
    image_3 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 3')
    image_4 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 4')
    image_5 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 5')
    image_6 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen Slide Banner 6')
    image_7 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen product 1')
    image_8 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen product 2')
    image_9 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen product 3')
    image_10 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen product 4')
    image_11 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen product 5')
    image_12 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen product 6')
    image_13 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen team 1')
    image_14 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen team 2')
    image_15 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen team 3')
    image_16 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen team 4')
    image_17 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='logo_parther')
    image_18 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='logo_parther')
    image_19 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='logo_parther')
    image_20 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='logo_parther')
    image_21 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='logo_parther')
    image_22 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='logo_parther')
    image_23 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='logo_parther')
    image_24 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='logo_parther')
    image_25 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='logo_parther')
    image_26 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='logo_parther')

    panels = [
        ImageChooserPanel('logo'),
        ImageChooserPanel('profile_pic'),
        ImageChooserPanel('image'),
        ImageChooserPanel('image_2'),
        ImageChooserPanel('image_3'),
        ImageChooserPanel('image_4'),
        ImageChooserPanel('image_5'),
        ImageChooserPanel('image_6'),
        ImageChooserPanel('image_7'),
        ImageChooserPanel('image_8'),
        ImageChooserPanel('image_9'),
        ImageChooserPanel('image_10'),
        ImageChooserPanel('image_11'),
        ImageChooserPanel('image_12'),
        ImageChooserPanel('image_13'),
        ImageChooserPanel('image_14'),
        ImageChooserPanel('image_15'),
        ImageChooserPanel('image_16'),
        ImageChooserPanel('image_17'),
        ImageChooserPanel('image_18'),
        ImageChooserPanel('image_19'),
        ImageChooserPanel('image_20'),
        ImageChooserPanel('image_21'),
        ImageChooserPanel('image_22'),
        ImageChooserPanel('image_23'),
        ImageChooserPanel('image_24'),
        ImageChooserPanel('image_25'),
        ImageChooserPanel('image_26'),
    ]




class ArticleListingPage(Page):
    template = "webapp/article_listing_page.html"

    custom_title = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        help_text='Overwrites the default title',
    )

    content_panels = Page.content_panels + [
        FieldPanel("custom_title"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["posts"] = ArticleDetailPage.objects.live().public()
        return context
    
class comments_ArticleDetailPage(AbstractFormField):
    page = ParentalKey('ArticleDetailPage', on_delete=models.CASCADE, related_name='form_fields')

class ArticleDetailPage(AbstractEmailForm):

    category = models.CharField(
        max_length=100,
        blank=False,
        null=True,
        help_text='Article category',
    )

    author = models.CharField(
        max_length=100,
        blank=False,
        null=True,
        help_text='Author Article',
    )

    bio2 = models.CharField(
        max_length=500,
        blank=False,
        null=True,
        help_text='Author bio',
    )

    custom_title = models.CharField(
        max_length=100,
        blank=False,
        null=True,
        help_text='Overwrites article title',
    )
    custom_subtitle = models.CharField(
        max_length=100,
        blank=False,
        null=True,
        help_text='Overwrites article subtitle',
    )
    blog_image = models.ForeignKey(
        "wagtailimages.Image",
        blank=False,
        null=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )
    date = models.DateTimeField(auto_now=True)
    abstract = RichTextField(blank=True,verbose_name='Abstract')
    comments = RichTextField(blank=True,verbose_name='Mensaje para que nos dejen un comentario')
    thank_you_text = RichTextField(blank=True)

    content = StreamField(
        [
            ("title_and_text", blocks.TitleAndTextBlock()),
            ("full_richtext", blocks.RichtextBlock()),
            ("simple_richtext", blocks.SimpleRichtextBlock()),
            ('image', ImageChooserBlock()),
            ("cards", blocks.CardBlock()),
        ],
        null=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("category"),
        FieldPanel("author"),
        FieldPanel("bio2"),
        FieldPanel("custom_title"),
        FieldPanel("custom_subtitle"),
        ImageChooserPanel("blog_image"),
        InlinePanel('galleria_article_Page', label="Imagenes del articulo"),
        FieldPanel("abstract"),
        StreamFieldPanel("content"),
        FormSubmissionsPanel(),
        InlinePanel('form_fields', label="comments"),
        FieldPanel('thank_you_text', classname="full"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], "Email"),
    ]

    def get_form_fields(self):
        return self.form_fields.all()

    def get_data_fields(self):
        data_fields = [
            ('name', 'Name'),
        ]
        data_fields += super().get_data_fields()

        return data_fields

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
    
class galleria_article_Page(Orderable):
    page = ParentalKey(ArticleDetailPage, on_delete=models.CASCADE, related_name='galleria_article_Page')    
    image_1 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Banner')
    image_2 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Author picture')
    image_3 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='imagen 2')
    
    
    panels = [
        ImageChooserPanel('image_1'),
        ImageChooserPanel('image_2'),
        ImageChooserPanel('image_3')
    ]

@register_setting
class SocialMediaArticleSettings(BaseSetting):
    facebook = models.URLField(blank=True,null=True,help_text="")
    twitter = models.URLField(blank=True,null=True,help_text="")
    instagram = models.URLField(blank=True,null=True,help_text="")
    youtube = models.URLField(blank=True,null=True,help_text="")
    pinterest = models.URLField(blank=True,null=True,help_text="")
    linkedin = models.URLField(blank=True,null=True,help_text="")

    panels = [
        MultiFieldPanel(
            [
            FieldPanel("facebook"),
            FieldPanel("twitter"),
            FieldPanel("instagram"),
            FieldPanel("youtube"),  
            FieldPanel("pinterest"),
            FieldPanel("linkedin"),         
            ]
        ,heading= "Social Media Settings Article")
    ]

JOBS= ( 
    ("Marketing & Publishing", "Marketing & Publishing"), 
    ("UI/UX Developer","UI/UX Developer"), 
    ("Python/Django Developer","Python/Django Developer"), 
    ("Docker Developer", "Docker Developer"), 
    ("Kubernetes Developer", "Kubernetes Developer"),
    ("FullStack Developer","FullStack Developer"),
    ("Chief Officer Technologies","Chief Officer Technologies"),
    ("Chief Officer", "Chief Officer"),
)


class JobsListingOpeningPage(Page):
    template = "webapp/joblistingopening.html"

    jobs_category= models.CharField(max_length=100, choices = JOBS, null=True)

    custom_title = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        help_text='Overwrites the default title',
    )

    benefits = RichTextField(blank=True,verbose_name='Beneficios')

    content_panels = Page.content_panels + [
        FieldPanel("custom_title"),
        FieldPanel("jobs_category"),
        FieldPanel("benefits"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["posts"] = JobsFormDetailOpeningPage.objects.live().public()
        return context

JOBS_CATEGORY= ( 
    ("Community Manager senior", "Community Manager senior"), 
    ("Community Manager Junior","Community Manager Juniorr"), 
    ("Content Designer senior","Content Designer senior"), 
    ("Content Designer junior", "Docker Developer junior"), 
    ("Project Manager senior", "Project Manager senior"),
    ("Project Manager junior","Project Manager junior"),
    ("UI/UX Desinger senior","UI/UX Desinger senior"),
    ("UI/UX Desinger junior","UI/UX Desinger junior"),
    ("Django Developer senior","Django Developer senior"),
    ("Django Developer junior","Django Developer junior"),
    ("System Reliability Engineer junior","System Reliability Engineer junior"),
    ("System Reliability Engineer senior","System Reliability Engineer senior"),
)


CITIES= ( 
    ("Quito", "Quito"), 
    ("Guayaquil","Guayaquil"), 
    ("Cuenca","Cuenca"), 
    ("Buenos Aires", "Buenos Aires"), 
    ("Mendoza", "Mendoza"),
    ("Paris","Paris"),
    ("Lausanne","Lausanne"),
    ("New York","New York"),
)

COUNTRY= ( 
    ("Ecuador", "Ecuador"), 
    ("Switzerland","Switzerland"), 
    ("Argentina","Argentina"), 
    ("France", "France"), 
    ("United States", "United States"),
)

TIMEJOBS= ( 
    ("Part Time", "Part Time"), 
    ("Full Time","Ful Time"), 
)
    
class JobsFormOpeningPage(AbstractFormField):
    field_type = models.CharField(
        verbose_name='field type',
        max_length=16,
        choices=list(FORM_FIELD_CHOICES) + [('image', 'Upload Image')]
    )
    
    page = ParentalKey('JobsFormDetailOpeningPage', on_delete=models.CASCADE, related_name='form_fields')


class CustomFormBuilder(FormBuilder):

    def create_image_field(self, field, options):
        return WagtailImageField(**options)

class JobsFormDetailOpeningPage(AbstractEmailForm):

    template = "webapp/jobdetailopening.html"


    jobs_category = models.CharField(max_length=100, choices = JOBS_CATEGORY, null=True)

    city= models.CharField(max_length=100, choices = CITIES, null=True)
    country = models.CharField(max_length=100, choices = COUNTRY, null=True)
    timejobs = models.CharField(max_length=100, choices = TIMEJOBS, null=True)
    description = RichTextField(blank=True,verbose_name='Descripción corta')
    uploadcv = models.FileField(upload_to='CV_file/%Y/%m/%d',null=True,blank=True)
    form_builder = CustomFormBuilder
    uploaded_image_collection = models.ForeignKey(
        'wagtailcore.Collection',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    def get_uploaded_image_collection(self):
        """
        Returns a Wagtail Collection, using this form's saved value if present,
        otherwise returns the 'Root' Collection.
        """
        collection = self.uploaded_image_collection
        return collection or Collection.get_first_root_node()

    @staticmethod
    def get_image_title(filename):
        """
        Generates a usable title from the filename of an image upload.
        Note: The filename will be provided as a 'path/to/file.jpg'
        """

        if filename:
            result = splitext(filename)[0]
            result = result.replace('-', ' ').replace('_', ' ')
            return result.title()
        return ''

    def process_form_submission(self, form):
        """
        Processes the form submission, if an Image upload is found, pull out the
        files data, create an actual Wgtail Image and reference its ID only in the
        stored form response.
        """

        cleaned_data = form.cleaned_data

        for name, field in form.fields.items():
            if isinstance(field, WagtailImageField):
                image_file_data = cleaned_data[name]
                if image_file_data:
                    ImageModel = get_image_model()

                    kwargs = {
                        'file': cleaned_data[name],
                        'title': self.get_image_title(cleaned_data[name].name),
                        'collection': self.get_uploaded_image_collection(),
                    }

                    if form.user and not form.user.is_anonymous:
                        kwargs['uploaded_by_user'] = form.user

                    image = ImageModel(**kwargs)
                    image.save()
                    # saving the image id
                    # alternatively we can store a path to the image via image.get_rendition
                    cleaned_data.update({name: image.pk})
                else:
                    # remove the value from the data
                    del cleaned_data[name]

        submission = self.get_submission_class().objects.create(
            form_data=json.dumps(form.cleaned_data, cls=DjangoJSONEncoder), # note: Wagtail 3.0 & beyond will no longer need to wrap this in json.dumps as it uses Django's JSONField under the hood now - https://docs.wagtail.org/en/stable/releases/3.0.html#replaced-form-data-textfield-with-jsonfield-in-abstractformsubmission
            page=self,
        )

        # important: if extending AbstractEmailForm, email logic must be re-added here
        if self.to_address:
            self.send_mail(form)

        return submission

        
    comments = RichTextField(blank=True,verbose_name='Mensaje para que nos dejen un comentario')
    thank_you_text = RichTextField(blank=True)

    content = StreamField(
        [
            ("title_and_text", blocks.TitleAndTextBlock()),
            ("full_richtext", blocks.RichtextBlock()),
            ("simple_richtext", blocks.SimpleRichtextBlock()),
            ('image', ImageChooserBlock()),
            ("cards", blocks.CardBlock()),
        ],
        null=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("jobs_category"),
        FieldPanel("city"),
        FieldPanel("country"),
        FieldPanel("timejobs"),
        FieldPanel("description"),
        FieldPanel('uploaded_image_collection'),
        StreamFieldPanel("content"),
        FormSubmissionsPanel(),
        InlinePanel('form_fields', label="comments"),
        FieldPanel('thank_you_text', classname="full"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], "Email"),
    ]

class ResourceslistingPage(Page):
    template = "webapp/resourceslisting.html"

    custom_title = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        help_text='Overwrites the default title',
    )

    content_panels = Page.content_panels + [
        FieldPanel("custom_title"),
        InlinePanel('galleria_resources_Page', label="Imagenes de background"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["posts"] = ResourcesDetailPage.objects.live().public()
        return context

class galleria_resources_Page(Orderable):
    page = ParentalKey(ResourceslistingPage, on_delete=models.CASCADE, related_name='galleria_resources_Page')    
    image = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Banner')

    panels = [
        ImageChooserPanel('image'),
    ]


class comments_ResourcesDetailPage(AbstractFormField):
    page = ParentalKey('ResourcesDetailPage', on_delete=models.CASCADE, related_name='form_fields')

TAGS= ( 
    ("Big Data", "Big Data"), 
    ("Data Science","Data Science"), 
    ("Machine Learning","Machine Learning"), 
    ("Cloud Infrastructure","Cloud Infrastructure"), 
    ("Intelligence Artificial","Intelligence Artificial"), 
)

class ResourcesDetailPage(AbstractEmailForm):
    template = "webapp/resourcesdetail.html"
    tags= models.CharField(max_length=100, choices = TAGS, null=True)
    delay = models.CharField( max_length=100,blank=False,null=True, help_text='delay time' )
    title_resource = models.CharField( max_length=100,blank=False,null=True, help_text='title_resource' )
    category = models.CharField( max_length=100,blank=False,null=True, help_text='Article category' )


    author = models.CharField(
        max_length=100,
        blank=False,
        null=True,
        help_text='Author Article',
    )

    bio2 = models.CharField(
        max_length=500,
        blank=False,
        null=True,
        help_text='Author bio',
    )

    custom_title = models.CharField(
        max_length=100,
        blank=False,
        null=True,
        help_text='Overwrites article title',
    )
    custom_subtitle = models.CharField(
        max_length=100,
        blank=False,
        null=True,
        help_text='Overwrites article subtitle',
    )
    blog_image = models.ForeignKey(
        "wagtailimages.Image",
        blank=False,
        null=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )
    date = models.DateTimeField(auto_now=True)
    abstract = RichTextField(blank=True,verbose_name='Abstract')
    comments = RichTextField(blank=True,verbose_name='Mensaje para que nos dejen un comentario')
    thank_you_text = RichTextField(blank=True)

    content = StreamField(
        [
            ("title_and_text", blocks.TitleAndTextBlock()),
            ("full_richtext", blocks.RichtextBlock()),
            ("simple_richtext", blocks.SimpleRichtextBlock()),
            ('image', ImageChooserBlock()),
            ("cards", blocks.CardBlock()),
        ],
        null=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("category"),
        FieldPanel("author"),
        FieldPanel("tags"),
        FieldPanel("delay"),
        FieldPanel("title_resource"),
        FieldPanel("bio2"),
        FieldPanel("custom_title"),
        FieldPanel("custom_subtitle"),
        ImageChooserPanel("blog_image"),
        InlinePanel('galleria_resourcedetail_Page', label="Imagenes de recursos"),
        FieldPanel("abstract"),
        StreamFieldPanel("content"),
        FormSubmissionsPanel(),
        InlinePanel('form_fields', label="comments"),
        FieldPanel('thank_you_text', classname="full"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], "Email"),
    ]

    def get_form_fields(self):
        return self.form_fields.all()

    def get_data_fields(self):
        data_fields = [
            ('name', 'Name'),
        ]
        data_fields += super().get_data_fields()

        return data_fields

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
    
class galleria_resourcedetail_Page(Orderable):
    page = ParentalKey(ResourcesDetailPage, on_delete=models.CASCADE, related_name='galleria_resourcedetail_Page')    
    image_1 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Banner')
    image_2 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Author picture')
    image_3 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='imagen 2')
    
    
    panels = [
        ImageChooserPanel('image_1'),
        ImageChooserPanel('image_2'),
        ImageChooserPanel('image_3')
    ]


class parnersPage(Page):
    template = "webapp/parthers.html"

    custom_title = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        help_text='Overwrites the default title',
    )

    content_panels = Page.content_panels + [
        FieldPanel("custom_title"),
        InlinePanel('partners_item_Page', label="partners"),
    ]

class partners_Page(Orderable):
    page = ParentalKey(parnersPage, on_delete=models.CASCADE, related_name='partners_item_Page')    
    partner_name = models.CharField(max_length=100,blank=False,null=True,help_text='Partner Name')
    partner_description = RichTextField(blank=True,verbose_name='Descripción del partner')
    partner_image = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Partner logo')

    
    
    panels = [
        FieldPanel("partner_name"),
        FieldPanel("partner_description"),
        ImageChooserPanel('partner_image')
    ]


class aboutusPage(Page):
    template = "webapp/aboutus.html"

    custom_title = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        help_text='Overwrites the default title',
    )
    aboutus= RichTextField(blank=True,verbose_name='SmartQuail Story')

    content_panels = Page.content_panels + [
        FieldPanel("custom_title"),
        FieldPanel("aboutus"),
        InlinePanel('aboutus_item_Page', label="teams"),
    ]

class aboutus_Page(Orderable):
    page = ParentalKey(aboutusPage, on_delete=models.CASCADE, related_name='aboutus_item_Page')    
    image_1 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='banner')
    image_2 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='profile_picture_1')
    image_3 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='profile_picture_2')
    image_4 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='profile_picture_3')
    image_5 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='profile_picture_4')
    image_6 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='profile_picture_5')
    image_7 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='profile_picture_6')
    team1_name = models.CharField(max_length=100,blank=False,null=False,help_text='Team 1 Name')
    team2_name = models.CharField(max_length=100,blank=False,null=False,help_text='Team 2 Name')
    team3_name = models.CharField(max_length=100,blank=False,null=False,help_text='Team 3 Name')
    team4_name = models.CharField(max_length=100,blank=False,null=False,help_text='Team 4 Name')
    team1_position = models.CharField(max_length=100,blank=False,null=False,help_text='Team 1 position')
    team2_position = models.CharField(max_length=100,blank=False,null=False,help_text='Team 2 position')
    team3_position = models.CharField(max_length=100,blank=False,null=False,help_text='Team 3 position')
    team4_position = models.CharField(max_length=100,blank=False,null=False,help_text='Team 4 position')

    panels = [
        ImageChooserPanel('image_1'),
        ImageChooserPanel('image_2'),
        ImageChooserPanel('image_3'),
        ImageChooserPanel('image_4'),
        ImageChooserPanel('image_5'),
        ImageChooserPanel('image_6'),
        ImageChooserPanel('image_7'),
        FieldPanel("team1_name"),
        FieldPanel("team2_name"),
        FieldPanel("team3_name"),
        FieldPanel("team4_name"),
        FieldPanel("team1_position"),
        FieldPanel("team2_position"),
        FieldPanel("team3_position"),
        FieldPanel("team4_position"),
    ]


PORFOLIO = ( 
    ("Landscapes", "Landscapes"), 
    ("Visual Production","Visual Production"), 
    ("web content","web content"), 
    ("Social Networks content","Social Networks content"), 
    ("Web Desing","Web Desing"), 
    ("Intelligence Artificial","Intelligence Artificial"), 
)

class contact_form_resume_Page(AbstractFormField):
    page = ParentalKey('ResumePage', on_delete=models.CASCADE, related_name='form_fields')

class ResumePage(AbstractEmailForm):


    template = "webapp/resume.html"

    custom_title = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        help_text='Nombre',
    )

    
    porfolio_1 = models.CharField(max_length=100, choices = PORFOLIO, null=True)
    porfolio_2 = models.CharField(max_length=100, choices = PORFOLIO, null=True)
    porfolio_3 = models.CharField(max_length=100, choices = PORFOLIO, null=True)
    porfolio_4 = models.CharField(max_length=100, choices = PORFOLIO, null=True)
    aboutus= RichTextField(blank=True,verbose_name='Acerca de mi')
    aboutus_1= RichTextField(blank=True,verbose_name='mensaje 1')
    aboutus_2= RichTextField(blank=True,verbose_name='mensaje 2')
    aboutus_3= RichTextField(blank=True,verbose_name='mensaje 3')
    experience_mesange  = models.CharField( max_length=100, blank=False, null=True,help_text='Describir un mensaje de experiencia',)
    educational_mesange  = models.CharField( max_length=100, blank=False, null=True,help_text='Describir un mensaje de la educación',)
    image = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Foto de perfil')
    comments = RichTextField(blank=True,verbose_name='Mensaje para que nos dejen un comentario')
    thank_you_text = RichTextField(blank=True)
    resume_url = models.URLField()

    content_panels = Page.content_panels + [
        FieldPanel("custom_title"),
        FieldPanel("aboutus"),
        FieldPanel("aboutus_1"),
        FieldPanel("aboutus_2"),
        FieldPanel("aboutus_3"),
        FieldPanel("porfolio_1"),
        FieldPanel("porfolio_2"),
        FieldPanel("porfolio_3"),
        FieldPanel("porfolio_4"),
        FieldPanel("resume_url"),
        FieldPanel("experience_mesange"),
        FieldPanel("educational_mesange"),
        ImageChooserPanel('image'),
        InlinePanel('porfolio_item_Page', label="porfolio"),
        InlinePanel('experiece_item_Page', label="experience"),
        InlinePanel('educational_item_Page', label="experience"),
        InlinePanel('form_fields', label="comments"),
        FieldPanel('thank_you_text', classname="full"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], "Email"),
    ]

class Porfolio_Page(Orderable):
    page = ParentalKey(ResumePage, on_delete=models.CASCADE, related_name='porfolio_item_Page')    
    porfolio_title = models.CharField( max_length=100, blank=False, null=True,help_text='Titulo de porfolio',)
    porfolio = models.CharField(max_length=100, choices = PORFOLIO, null=True)
    image_1 = models.ForeignKey('wagtailimages.Image',null=True,blank=True,on_delete=models.SET_NULL,related_name='+',verbose_name='Imagen 1')
 

    panels = [
        FieldPanel("porfolio_title"),
        FieldPanel("porfolio"),
        ImageChooserPanel('image_1'),

    ]

class Experience_Page(Orderable):
    page = ParentalKey(ResumePage, on_delete=models.CASCADE, related_name='experiece_item_Page')    
    business_title = models.CharField( max_length=100, blank=False, null=True,help_text='Nombre de la empresa donde trabajo',)
    business_chage = models.CharField( max_length=100, blank=False, null=True,help_text='Nombre del cargo que ocupo',)
    business_activity = models.CharField( max_length=1000, blank=False, null=True,help_text='Descripcion de la actividad realizada',)
    Fecha = models.DateTimeField()
 

    panels = [
        FieldPanel("business_title"),
        FieldPanel("business_chage"),
        FieldPanel("business_activity"),
        FieldPanel("Fecha"),
    ]

class Educational_Page(Orderable):
    page = ParentalKey(ResumePage, on_delete=models.CASCADE, related_name='educational_item_Page')    
    academy_title = models.CharField( max_length=100, blank=False, null=True,help_text='Nombre de la institución educativa',)
    title = models.CharField( max_length=100, blank=False, null=True,help_text='Nombre del titulo',)
    academy_activity = models.CharField( max_length=1000, blank=False, null=True,help_text='Descripcion de la formación',)
    Fecha = models.DateTimeField()
 

    panels = [
        FieldPanel("academy_title"),
        FieldPanel("title"),
        FieldPanel("academy_activity"),
        FieldPanel("Fecha"),
    ]







@register_setting
class SocialMediaTeam1Settings(BaseSetting):
    facebook = models.URLField(blank=True,null=True,help_text="")
    twitter = models.URLField(blank=True,null=True,help_text="")
    instagram = models.URLField(blank=True,null=True,help_text="")
    youtube = models.URLField(blank=True,null=True,help_text="")
    pinterest = models.URLField(blank=True,null=True,help_text="")
    linkedin = models.URLField(blank=True,null=True,help_text="")

    panels = [
        MultiFieldPanel(
            [
            FieldPanel("facebook"),
            FieldPanel("twitter"),
            FieldPanel("instagram"),
            FieldPanel("youtube"),  
            FieldPanel("pinterest"),
            FieldPanel("linkedin"),         
            ]
        ,heading= "Social Media Settings-1")
    ]

@register_setting
class SocialMediaTeam2Settings(BaseSetting):
    facebook = models.URLField(blank=True,null=True,help_text="")
    twitter = models.URLField(blank=True,null=True,help_text="")
    instagram = models.URLField(blank=True,null=True,help_text="")
    youtube = models.URLField(blank=True,null=True,help_text="")
    pinterest = models.URLField(blank=True,null=True,help_text="")
    linkedin = models.URLField(blank=True,null=True,help_text="")

    panels = [
        MultiFieldPanel(
            [
            FieldPanel("facebook"),
            FieldPanel("twitter"),
            FieldPanel("instagram"),
            FieldPanel("youtube"),  
            FieldPanel("pinterest"),
            FieldPanel("linkedin"),         
            ]
        ,heading= "Social Media Settings-2")
    ]

@register_setting
class SocialMediaTeam3Settings(BaseSetting):
    facebook = models.URLField(blank=True,null=True,help_text="")
    twitter = models.URLField(blank=True,null=True,help_text="")
    instagram = models.URLField(blank=True,null=True,help_text="")
    youtube = models.URLField(blank=True,null=True,help_text="")
    pinterest = models.URLField(blank=True,null=True,help_text="")
    linkedin = models.URLField(blank=True,null=True,help_text="")

    panels = [
        MultiFieldPanel(
            [
            FieldPanel("facebook"),
            FieldPanel("twitter"),
            FieldPanel("instagram"),
            FieldPanel("youtube"),  
            FieldPanel("pinterest"),
            FieldPanel("linkedin"),         
            ]
        ,heading= "Social Media Settings-3")
    ]

@register_setting
class SocialMediaTeam4Settings(BaseSetting):