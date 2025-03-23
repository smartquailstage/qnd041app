from .models import Product, Category
from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register


@register(Product)
class Products(TranslationOptions):
    fields = ('name','slug','image')


@register(Category)
class Category(TranslationOptions):
    fields = ('name','slug','salidas','image','desde','description','detail','terms')


