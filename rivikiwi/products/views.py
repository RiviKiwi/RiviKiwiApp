from django.shortcuts import render
from .models import Product, ProductCategory

def index(request, category_slug):
    category = ProductCategory.objects.get(slug=category_slug)
    products = Product.objects.all() if category_slug == "all" else Product.objects.filter(category__slug=category_slug)
    context = {
        'products':products,
        'category':category,
    }
    return render(request, 'products/index.html', context)

def product(request, product_slug):
    
    product = Product.objects.get(slug=product_slug)
    
    context = {
        'product':product,    
    }
    return render(request, 'products/product.html', context)