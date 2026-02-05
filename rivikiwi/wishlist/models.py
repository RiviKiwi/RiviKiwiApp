from django.db import models
from rivikiwi import settings
from products.models import Product


class WishlistItem(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    product = models.ForeignKey(
        to=Product, on_delete=models.CASCADE, verbose_name="Продукт"
    )
    add_date = models.DateField(auto_now_add=True, verbose_name="Дата добавления")

    class Meta:
        db_table = "wishlist"
        verbose_name = "Список желаемого"
        verbose_name_plural = "Списки желаемого"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "product"], name="unique_product_in_wishlist"
            )
        ]
