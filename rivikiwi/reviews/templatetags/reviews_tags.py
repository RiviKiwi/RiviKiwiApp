from django import template
from reviews.utils import seller_reviews

register = template.Library()

@register.simple_tag()
def get_seller_reviews(seller_id):
    return seller_reviews(seller_id)