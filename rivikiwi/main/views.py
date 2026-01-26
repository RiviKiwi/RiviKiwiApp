from django.shortcuts import render
from products.models import Product

def index(request):
    city = request.GET.get("city", None)
    products = Product.objects.all()
    
    if city:
        products = products.filter(city__name=city)
    
    context = {
        'products':products,
    }
    return render(request, 'main/index.html', context)
