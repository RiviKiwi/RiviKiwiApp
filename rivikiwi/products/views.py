from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Product, ProductCategory
from .utils import q_search

def index(request, category_slug=None):
    max_price = request.GET.get("max_price", None)
    min_price = request.GET.get("min_price", None)
    rating = request.GET.get("rating", None)
    has_discount = request.GET.get("has_discount", None)
    order_by = request.GET.get("order_by", None)
    city = request.GET.get("city", None)
    query = request.GET.get("q", None)
    page = request.GET.get("page", 1)
    print(query)
    
    # if not category_slug:
    #     category_slug = "all"
        
    category = ProductCategory.objects.get(slug=category_slug) if category_slug else None
    products = None
    
    if category_slug == "all" or (not query and not category_slug): 
        products = Product.objects.all()
        category = category = ProductCategory.objects.get(slug="all")
    elif query:
        products = q_search(query) 
    else:
        products = Product.objects.filter(category__slug=category_slug)
    
    if order_by:
        products = products.order_by(order_by)
        
    if city:
        products = products.filter(city__name=city)
        
    if min_price and min_price != '0':
        products = products.filter(price__gte=int(min_price))
        
    if max_price and max_price != '0':
        products = products.filter(price__lte=int(max_price))
        
    if rating:
        products = products.filter(rating__gte=float(rating))
        
    if has_discount:
        products = products.filter(discount__gt=0)
        
    paginator = Paginator(products, 3)
    page = paginator.page(page)
    
    context = {
        'products':page,
        'category':category,
    }
    return render(request, 'products/index.html', context)

def product(request, product_slug):
    
    product = Product.objects.get(slug=product_slug)
    
    context = {
        'product':product,    
    }
    return render(request, 'products/product.html', context)