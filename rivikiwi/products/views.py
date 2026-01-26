from django.shortcuts import render
from .models import Product, ProductCategory

def index(request, category_slug):
    order_by = request.GET.get("order_by", None)
    city = request.GET.get("city", None)
    
    category = ProductCategory.objects.get(slug=category_slug)
    products = Product.objects.all() if category_slug == "all" else Product.objects.filter(category__slug=category_slug)
    
    if order_by:
        products = products.order_by(order_by)
        
    if city:
        products = products.filter(city__name=city)
    
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