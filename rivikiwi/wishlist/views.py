from django.shortcuts import render

def wishlist(request):
    return render(request, "wishlist/wishlist.html")
