from django import template
from products.models import ProductCategory, City
from django.utils.http import urlencode

register = template.Library()

@register.simple_tag()
def all_categories():
    return ProductCategory.objects.all()

@register.simple_tag()
def all_cities():
    return City.objects.all()

@register.simple_tag(takes_context=True)
def change_params(context, **kwargs):
    query = context['request'].GET.dict()
    query.update(kwargs)
    return urlencode(query)