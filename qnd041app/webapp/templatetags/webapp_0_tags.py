from django import template
from django.template.loader import get_template
from django.template.defaultfilters import stringfilter
from wagtailmenus.models import FlatMenu
register = template.Library()
 
@register.tag
def slider(parser, token):
    nodelist = parser.parse(('endslider',))
    parser.delete_first_token()
    return SliderNode(nodelist)
 
class SliderNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist
 
    def render(self, context):
        output = self.nodelist.render(context)
        return output

@register.tag
def header(parser, token):
    try:
        tag_name, modal_id, title = token.split_contents()
    except ValueError:
        raise TemplateSyntaxError("%r takes two arguments: the modal id and title" % token.contents.split()[0])
 
    nodelist = parser.parse(('endheader',))
    parser.delete_first_token()
    return headerNode(modal_id, title, nodelist)
 
@register.tag
def header(parser, token):
    nodelist = parser.parse(('endheader',))
    parser.delete_first_token()
    return HeaderNode(nodelist)


class HeaderNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        output = self.nodelist.render(context(**kwargs))
        t = template.loader.get_template('webapp_0/header.html')
        c = template.Context({'body': output})
        return t.render(c)

@register.tag
def portfolio(parser, token):
    nodelist = parser.parse(('endportfolio',))
    parser.delete_first_token()
    return portfolioNode(nodelist)
 
class portfolioNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist
 
    def render(self, context):
        output = self.nodelist.render(context)
        return output

@register.tag
def tearsheeting(parser, token):
    nodelist = parser.parse(('endtearsheeting',))
    parser.delete_first_token()
    return tearsheetingNode(nodelist)
 
class tearsheetingNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist
 
    def render(self, context):
        output = self.nodelist.render(context)
        return output

@register.tag
def noticias(parser, token):
    nodelist = parser.parse(('endnoticias',))
    parser.delete_first_token()
    return noticiasNode(nodelist)
 
class noticiasNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist
 
    def render(self, context):
        output = self.nodelist.render(context)
        return output

@register.tag
def contact(parser, token):
    nodelist = parser.parse(('endcontact',))
    parser.delete_first_token()
    return contactNode(nodelist)
 
class contactNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist
 
    def render(self, context):
        output = self.nodelist.render(context)
        return output

@register.tag
def footer(parser, token):
    nodelist = parser.parse(('endfooter',))
    parser.delete_first_token()
    return footerNode(nodelist)
 
class footerNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist
 
    def render(self, context):
        output = self.nodelist.render(context)
        return output
    
#Menus
#Products

@register.simple_tag
def smartbusinessmedia_menus():
    return FlatMenu.objects.filter(handle__endswith='smartbusinessmedia')

@register.simple_tag
def smartbusinessanalytics_menus():
    return FlatMenu.objects.filter(handle__endswith='smartbusinessanalytics')

@register.simple_tag
def smartbusinesstechnologies_menus():
    return FlatMenu.objects.filter(handle__endswith='smartbusinesstechnologies')

@register.simple_tag
def smartbusinesslaw_menus():
    return FlatMenu.objects.filter(handle__endswith='smartbusinesslaw')

#solutions

@register.simple_tag
def bycategory_menus():
    return FlatMenu.objects.filter(handle__endswith='bycategory')

@register.simple_tag
def byorganizationtype_menus():
    return FlatMenu.objects.filter(handle__endswith='byorganizationtype')

@register.simple_tag
def bycustomer_menus():
    return FlatMenu.objects.filter(handle__endswith='bycustomer')

#training&jobs

@register.simple_tag
def training_menus():
    return FlatMenu.objects.filter(handle__endswith='training')

@register.simple_tag
def jobs_menus():
    return FlatMenu.objects.filter(handle__endswith='jobs')

#Resources

@register.simple_tag
def ourvision_menus():
    return FlatMenu.objects.filter(handle__endswith='ourvision')

@register.simple_tag
def topics_menus():
    return FlatMenu.objects.filter(handle__endswith='topics')

@register.simple_tag
def articles_menus():
    return FlatMenu.objects.filter(handle__endswith='articles')

@register.simple_tag
def news_menus():
    return FlatMenu.objects.filter(handle__endswith='news')

#parthers

@register.simple_tag
def forcustomers_menus():
    return FlatMenu.objects.filter(handle__endswith='forcustomers')

@register.simple_tag
def forpartners_menus():
    return FlatMenu.objects.filter(handle__endswith='forpartners')

#about

@register.simple_tag
def aboutus_menus():
    return FlatMenu.objects.filter(handle__endswith='aboutus')

@register.simple_tag
def opensource_menus():
    return FlatMenu.objects.filter(handle__endswith='opensource')
@register.simple_tag
def companydetails_menus():
    return FlatMenu.objects.filter(handle__endswith='companydetails')

@register.simple_tag
def communities_menus():
    return FlatMenu.objects.filter(handle__endswith='communities')


#footer

@register.simple_tag
def workwithus_menus():
    return FlatMenu.objects.filter(handle__endswith='workwithus')

@register.simple_tag
def usefullinks_menus():
    return FlatMenu.objects.filter(handle__endswith='usefullinks')

@register.simple_tag
def contactus_menus():
    return FlatMenu.objects.filter(handle__endswith='contactus')

