from django import template
from products.models import ProductCategory

register = template.Library()

@register.simple_tag()
def all_categories():
    return ProductCategory.objects.all()