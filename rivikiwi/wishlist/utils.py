from .models import WishlistItem
from django.db.models import Q

def is_in_wishlist(product, user):
    if not user.is_authenticated:
        return False
    
    return WishlistItem.objects.filter(
        Q(user=user) & Q(product=product)
    ).exists()