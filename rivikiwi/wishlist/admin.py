from django.contrib import admin
from wishlist.models import WishlistItem


class WishlistTabAdmin(admin.TabularInline):
    model = WishlistItem
    fields = ("product", "add_date")
    search_fields = ("product", "add_date")
    readonly_fields = ("add_date",)
    extra = 1


@admin.register(WishlistItem)
class WishlistItemAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "product", "add_date"]
    search_fields = ["id", "user", "add_date"]

    def product_display(self, obj):
        return str(obj.product)

    def user_display(self, obj):
        return str(obj.user)
