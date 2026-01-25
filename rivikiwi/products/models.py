from django.db import models
from django.conf import settings

class ProductCategory(models.Model):
    name = models.CharField(
        max_length=35, blank=True, null=True, unique=True, verbose_name="Название"
    )
    slug = models.SlugField(unique=True, verbose_name="url")

    class Meta:
        db_table = "product_category"
        verbose_name = "категорию"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        max_length=100, blank=True, null=True, unique=True, verbose_name="Название"
    )
    slug = models.SlugField(unique=True, verbose_name="url")
    category = models.ForeignKey(
        to=ProductCategory, on_delete=models.CASCADE, verbose_name="Категория"
    )
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="Цена")
    discount = models.PositiveIntegerField(blank=True, null=True, verbose_name="Скидка")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь")

    class Meta:
        db_table = "products"
        verbose_name = "продукт"
        verbose_name_plural = "Продукты"

    def __str__(self):
        return self.name
    
    def get_price(self):
        if self.discount:
            return self.price * self.discount
        
        return self.price
    
    def get_first_picture(self):
        res_image = self.images.all().first()
        if res_image:
            return res_image.image
        return None


class ProductImage(models.Model):
    product = models.ForeignKey(to=Product,on_delete=models.CASCADE, related_name="images", verbose_name="Продукт")
    image = models.ImageField(upload_to="product_images", verbose_name="Изображение")
    is_main = models.BooleanField(default=False, verbose_name="Главное изображение")

    class Meta:
        db_table = "product_images"
        verbose_name = "изображение товара"
        verbose_name_plural = "Изображения товара"
