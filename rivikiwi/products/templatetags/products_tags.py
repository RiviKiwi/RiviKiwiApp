from django import template
from products.models import ProductCategory, City, Product
from django.utils.http import urlencode
from wishlist.utils import is_in_wishlist
register = template.Library()

@register.simple_tag()
def all_categories():
    return ProductCategory.objects.all()

@register.simple_tag()
def all_cities():
    return City.objects.all()

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