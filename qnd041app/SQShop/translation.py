from .models import Product, Category
from modeltranslation.translator import translator, TranslationOptions
from modeltranslation.decorators import register


@register(Product)
class Products(TranslationOptions):
    fields = ('name','slug','image')


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = (
        'nombre',
        'slug',
        'software',
        'plataforma',
        'numero_procesos',
        'automatizacion',
        'inteligencia_artificial',
        'latencia_aproximada',
        'usuarios_simultaneos',
    )

