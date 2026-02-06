from django.http import HttpResponseRedirect
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from wishlist.models import WishlistItem
from django.views.generic import View
from products.models import Product


class WishlistView(LoginRequiredMixin, ListView):
    model = WishlistItem
    template_name = "wishlist/wishlist.html"
    context_object_name = "wishlist"

    def get_queryset(self):
        return WishlistItem.objects.filter(user=self.request.user)


class AddWishlistView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        user = self.request.user
        product_id = self.kwargs.get("product_id")
        product = Product.objects.get(id=product_id)

        WishlistItem.objects.create(user=user, product=product)

        source_page = self.request.META["HTTP_REFERER"]

        return HttpResponseRedirect(source_page)


class DeleteWishlistView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        user = self.request.user
        product_id = self.kwargs.get("product_id")
        product = Product.objects.get(id=product_id)

        WishlistItem.objects.get(user=user, product=product).delete()

        source_page = self.request.META["HTTP_REFERER"]

        return HttpResponseRedirect(source_page)
