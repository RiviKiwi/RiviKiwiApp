from django.shortcuts import render
from .models import Product

def index(request, category_slug):
    products = Product.objects.all() if category_slug == "all" else Product.objects.filter(category__slug=category_slug)
    context = {
        'products':products,
    }
    return render(request, 'products/index.html', context)

def product(request, product_slug):
    context = {
        
    }
    return render(request, 'main/index.html', context)