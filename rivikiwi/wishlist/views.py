from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from wishlist.models import WishlistItem


class WishlistView(LoginRequiredMixin, ListView):
    model = WishlistItem
    template_name = "wishlist/wishlist.html"
    context_object_name = "wishlist"

    def get_queryset(self):
        return WishlistItem.objects.filter(user=self.request.user)
