from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField
from sbmcoupons.models import Coupon

class Category(models.Model):
    name = models.CharField(max_length=200,
                            db_index=True)
    slug = models.SlugField(max_length=200,
                            unique=True)
    logo = models.ImageField(upload_to='logo/%Y/%m/%d',
                              blank=True,null=True)
    title = models.CharField(max_length=250, null=True, blank=True)

    TECH_TYPE = (
    ("Investigación y Desarollo", "(I+D)"),
    ("Automatizacion", "(+A)+(I+D)"),
    ("Inteligencia Artificial", "(+AI)+(I+D)"),
    ("Automatizacion y Inteligencia Artificial", "(+A)+(+AI)+(I+D)"),

    )

    tech_type= models.CharField(choices=TECH_TYPE, max_length=200, db_index=True,null=True, blank= True)

    sbmmodels_p1 = RichTextField(blank=True)
    sbmmodels_p2 = RichTextField(blank=True)
    sbmmodels_p3 = RichTextField(blank=True)


    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
            return reverse('sbmshop:product_list_by_category',
                           args=[self.slug])


class SBMProduct(models.Model):
    ICON_CHOICE = (
    ("icofont-legal", "icofont-legal"),
    ("icofont-law-book", "icofont-law-book"),
    ("icofont-ebook", "icofont-ebook"),
    ("icofont-ui-office", "icofont-ui-office"),
    ("icofont-list", "icofont-list"),
    ("icofont-key", "icofont-key"),
    )
    
    COLORS_CHOICE = (
    ("rgb(133, 54, 140)", "SBM-CRM+AI+I+D"),
    ("#262625", "SBM-CRM"),
    ("#662d14", "SBM-CRM+A"),
    ("#247832", "SBM-CRM+I+D"),
    ("#7c7a21", "SBM-CRM+A+I+D"),
    ("#283f75", "SBM-CRM+AI"),
    ("#388e86", "SBM-CRM+A+AI"),
    ("#251f25", "SBM-CRM+A+AI+I+D"),
    )
  

    category = models.ForeignKey(Category,
                                 related_name='products',
                                 on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupon,
                                 related_name='coupon',
                                 on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='products/smartbusinessmedia/bannering/%Y/%m/%d',
                              blank=True)
    image1 = models.ImageField(upload_to='products/smartbusinessmedia/scren1/%Y/%m/%d',
                              blank=True)
    image2 = models.ImageField(upload_to='products/smartbusinessmedia/scren2/%Y/%m/%d',
                              blank=True)
    image3 = models.ImageField(upload_to='products/smartbusinessmedia/scren3/%Y/%m/%d',
                              blank=True)
    background = models.ImageField(upload_to='products/smartbusinessmedia/background/%Y/%m/%d',
                              blank=True)
    coupon = models.ForeignKey(Coupon,
                                 related_name='coupon',
                                 on_delete=models.CASCADE,null=True,blank=True)

    
    item1 = models.TextField(blank=True,null=True)
    item2 = models.TextField(blank=True,null=True)
    item3 = models.TextField(blank=True,null=True)
    item4 = models.TextField(blank=True,null=True)

    description =RichTextField(blank=True)
    datasheet = models.TextField(blank=True)
    terms_policies =RichTextField(blank=True)
    cloud_requirements =RichTextField(blank=True)
    terms_conditions = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    icon= models.CharField(choices=ICON_CHOICE, max_length=200, db_index=True,null=True, blank= True)
    color = models.CharField(choices=COLORS_CHOICE, max_length=200, db_index=True,null=True, blank= True)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
            return reverse('sbmshop:product_detail',
                           args=[self.id, self.slug])

    def get_staff(self):
        """Devuelve los miembros del personal relacionados con este producto."""
        return self.technologies_products.all()

    def get_technologies(self):
        """Devuelve las tecnologías relacionadas con este producto."""
        return self.technologies_products.all()


class SBMStaffItem(models.Model):

    COLORS_CHOICE = (
    ("SmartBusinessMedia Community Manager", "SmartBusinessMedia Community Manager"),
    ("Chief Officer of Technologies", "Chief Officer of Technologies"),
    ("SmartBusinessMedia Project Manager", "SmartBusinessMedia Project Manager"),
    ("Chief Officer SmartBusinessMedia", "Chief Officer SmartBusinessMedia "),

    )
    sbmproducts = models.ForeignKey(SBMProduct,
                                 related_name='staffproducts',
                                 on_delete=models.CASCADE)
    ceo_name = models.CharField(max_length=200, db_index=True)
    ceo_lastname = models.CharField(max_length=200, db_index=True)
    ceo_sector = models.CharField(choices=COLORS_CHOICE, max_length=200, db_index=True)
    ceo_profile_img= models.ImageField(upload_to='products/smartbusinessmedia/sbmstaff/%Y/%m/%d',
                              blank=True)

    def __str__(self):
        return '{}'.format(self.id)

class SBMTechnologiesItem(models.Model):
    PLATAFORM_CHOICE = (
    ("Simple IT Cloud Web App+CRM", "Simple IT Cloud Web App+CRM"),
    ("Simple IT Cloud Web App+CRM+I+D", "Simple IT Cloud Web App+CRM+I+D"),
    ("Simple IT Cloud Web App+CRM+I+D+A", "Simple IT Cloud Web App+CRM+I+D+A"),
    ("Simple IT Cloud Web App+CRM+A", "Simple IT Cloud Web App+CRM+A"),
    ("Simple IT Cloud Web App+CRM+AI", "Simple IT Cloud Web App+CRM+AI"),
    ("Simple IT Cloud Web App+CRM+AI+A", "Simple IT Cloud Web App+CRM+AI+A"),
    ("Simple IT Cloud Web App+CRM+AI+I+D", "Simple IT Cloud Web App+CRM+AI+I+D"),
    ("Simple IT Cloud Web App+CRM+AI+A+I+D", "Simple IT Cloud Web App+CRM+AI+A+I+D"),

    )
    RELIEBLE = (
        ("Low ", "Low"),
        ("Medium", "Medium"),
        ("High", "High"),

    )
    logo_img = models.ImageField(upload_to='products/smartbusinessmedia/sbmtechnologies/%Y/%m/%d',
                              blank=True,null=True)
    sbmproductstechno = models.ForeignKey(SBMProduct,
                                 related_name='technologies_products',
                                 on_delete=models.CASCADE)
    version = models.CharField(max_length=200, db_index=True,null=True,blank=True)
    Node_name = models.CharField(max_length=200, db_index=True,null=True,blank=True)
    App_type = models.CharField(choices=PLATAFORM_CHOICE, max_length=500, db_index=True,null=True,blank=True)
    Domain= models.CharField(max_length=200, db_index=True,null=True,blank=True)
    Types_reliable_systems = models.CharField(choices=RELIEBLE, max_length=500, db_index=True,null=True,blank=True)
    procesing_resourse = models.CharField(max_length=200, db_index=True,null=True,blank=True)
    memory_resourse = models.CharField(max_length=200, db_index=True,null=True,blank=True)
    storge_resourse = models.CharField(max_length=200, db_index=True,null=True,blank=True)


 

    def __str__(self):
        return '{}'.format(self.Node_name)




class SBMProductManual(models.Model):

    COLORS_CHOICE = (
    ("rgb(133, 54, 140)", "SBM-CRM+AI+I+D"),
    ("#0d0d0d", "SBM-CRM"),
    ("#662d14", "SBM-CRM+A"),
    ("#247832", "SBM-CRM+I+D"),
    ("#7c7a21", "SBM-CRM+A+I+D"),
    ("#283f75", "SBM-CRM+AI"),
    ("#388e86", "SBM-CRM+A+AI"),
    ("#251f25", "SBM-CRM+A+AI+I+D"),
    )
    
    product  = models.ForeignKey(SBMProduct,
                                 related_name='products',
                                 on_delete=models.CASCADE)

    category = models.ForeignKey(Category,
                                 related_name='categories',
                                 on_delete=models.CASCADE)

    logo_image = models.ImageField(upload_to='products/smartbusinessmedia/background/%Y/%m/%d',
                              blank=True)

    bg_image = models.ImageField(upload_to='products/smartbusinessmedia/background/%Y/%m/%d',
                              blank=True)

    color = models.CharField(choices=COLORS_CHOICE, max_length=200, db_index=True,null=True, blank= True)

    title_intro = models.CharField(max_length=200, db_index=True,null=True,blank=True)
    subtitle_title_intro = models.CharField(max_length=200, db_index=True,null=True,blank=True)
    text = models.TextField(blank=True)


class ManualItem(models.Model):
    manuales = models.ForeignKey(SBMProductManual,
                              related_name='items',
                              on_delete=models.CASCADE)

    title_intro = models.CharField(max_length=200, db_index=True,null=True,blank=True)
    subtitle_title_intro = models.CharField(max_length=200, db_index=True,null=True,blank=True)
    text = models.TextField(blank=True)


    def __str__(self):
        return '{}'.format(self.id)


