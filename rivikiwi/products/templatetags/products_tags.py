from django import template
from products.models import ProductCategory, City

register = template.Library()

@register.simple_tag()
def all_categories():
    return ProductCategory.objects.all()

@register.simple_tag()
def all_cities():
    return City.objects.all()