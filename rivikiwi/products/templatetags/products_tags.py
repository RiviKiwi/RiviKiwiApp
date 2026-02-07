from django import template
from products.models import ProductCategory, City, Product
from django.utils.http import urlencode
from wishlist.utils import is_in_wishlist
from django.core.cache import cache
register = template.Library()

@register.simple_tag()
def all_categories():
    categories = cache.get('categories')
    if not categories:
        categories = ProductCategory.objects.all()
        cache.set('categories', categories, 500)
    return categories

@register.simple_tag()
def all_cities():
    cities = cache.get('cities')
    if not cities:
        cities = City.objects.all()
        cache.set('cities', cities, 500)
    return cities

@register.simple_tag(takes_context=True)
def all_user_products(context):
    seller = context.get('seller', None)
    if seller:
        return Product.objects.filter(user=seller)
    
    return Product.objects.filter(user=context['user'])

@register.simple_tag(takes_context=True)
def change_params(context, **kwargs):
    query = context['request'].GET.dict()
    query.update(kwargs)
    return urlencode(query)

@register.simple_tag()
def is_in_wishlist_tag(product, user):
    return is_in_wishlist(product, user)