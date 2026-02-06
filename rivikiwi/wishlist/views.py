from django.http import HttpResponseRedirect
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from wishlist.models import WishlistItem
from django.views.generic import View
from products.models import Product, ProductCategory
from django.urls import reverse_lazy
from .utils import is_in_wishlist

class WishlistView(LoginRequiredMixin, ListView):
    model = WishlistItem
    template_name = "wishlist/wishlist.html"
    context_object_name = "wishlist"

    def get_queryset(self):
        return WishlistItem.objects.filter(user=self.request.user)


class WorkWithWishlistView(LoginRequiredMixin,View):
    
    def post(self, request, *args, **kwargs):
        
        user = self.request.user
        product_id = self.kwargs.get('product_id')
        product = Product.objects.get(id=product_id)
        is_like = is_in_wishlist(product, user)
        
        if not is_like:
            WishlistItem.objects.create(user=user, product=product)
        else:
            WishlistItem.objects.get(user=user, product=product).delete()

        name_of_page = self.request.META["HTTP_REFERER"]
        
        
        return HttpResponseRedirect(name_of_page)

        
        
