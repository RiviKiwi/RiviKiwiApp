from django.shortcuts import render
from products.models import Product

def index(request):
    products = Product.objects.all()
    
    context = {
        'products':products,
    }
    return render(request, 'main/index.html', context)
