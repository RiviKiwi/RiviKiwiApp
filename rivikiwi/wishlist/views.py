import logging
from django.http import HttpResponseRedirect
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from wishlist.models import WishlistItem
from django.views.generic import View
from products.models import Product

logger  = logging.getLogger('wishlist_app')

class WishlistView(LoginRequiredMixin, ListView):
    model = WishlistItem
    template_name = "wishlist/wishlist.html"
    context_object_name = "wishlist"

    def get_queryset(self):
        logger.info("Get all WishlistItem connected with request user")
        return WishlistItem.objects.filter(user=self.request.user)


class AddWishlistView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        logger.debug("Try to add product to user wishlist")
        
        user = self.request.user
        logger.info("Get user from request")
        
        product_id = self.kwargs.get("product_id")
        logger.info("Get product_id from kwargs")
        
        product = Product.objects.get(id=product_id)
        logger.info("Get product by product_id")

        WishlistItem.objects.create(user=user, product=product)
        logger.warning("Add product to user wishlist")

        source_page = self.request.META["HTTP_REFERER"]
        logger.warning("Get source page and redirect to this page")
        
        return HttpResponseRedirect(source_page)


class DeleteWishlistView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        logger.debug("Try to delete product from user wishlist")
        
        user = self.request.user
        logger.info("Get user from request")
        
        product_id = self.kwargs.get("product_id")
        logger.info("Get product_id from kwargs")
        
        product = Product.objects.get(id=product_id)
        logger.info("Get product by product_id")

        WishlistItem.objects.get(user=user, product=product).delete()
        logger.warning("Delete product from user wishlist")

        source_page = self.request.META["HTTP_REFERER"]
        logger.warning("Get source page and redirect to this page")

        return HttpResponseRedirect(source_page)
