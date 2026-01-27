
from .models import Product
def q_search(query):
    return Product.objects.all()