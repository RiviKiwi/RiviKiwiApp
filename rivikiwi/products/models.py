from django.db import models
from django.conf import settings
from django.utils.text import slugify


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


class City(models.Model):
    name = models.CharField(
        max_length=35, blank=True, null=True, unique=True, verbose_name="Город"
    )
    slug = models.SlugField(unique=True, blank=True, null=True, verbose_name="url")

    class Meta:
        db_table = "city"
        verbose_name = "город"
        verbose_name_plural = "Города"
        
    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Название"
    )
    slug = models.SlugField(unique=True, verbose_name="url")
    category = models.ForeignKey(
        to=ProductCategory, on_delete=models.CASCADE, verbose_name="Категория"
    )
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="Цена")
    discount = models.PositiveIntegerField(blank=True, null=True, verbose_name="Скидка")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    city = models.ForeignKey(to=City, on_delete=models.CASCADE, related_name="city", verbose_name="Город")
    creation_date = models.DateField(auto_now_add=True, verbose_name="Дата создания")
    
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

    def get_images(self):
        res_images = self.images.all()
        return res_images if res_images else None
    
    def save(self, *args, **kwargs):
        new_slug = f"product-{self.category}-{self.name}"
        unique_slug = slugify(new_slug)
        counter = 1
        original_slug = unique_slug
        while self.__class__.objects.filter(slug=unique_slug).exists():
            unique_slug = f"{original_slug}-{counter}"
            counter += 1

        self.slug = unique_slug
        super().save(*args, **kwargs)
    
        
    def get_count_of_views(self):
        return len(self.views.all()) if self.views.all() else 0

class ProductImage(models.Model):
    product = models.ForeignKey(
        to=Product,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name="Продукт",
    )
    image = models.ImageField(upload_to="product_images", verbose_name="Изображение")
    is_main = models.BooleanField(default=False, verbose_name="Главное изображение")

    class Meta:
        db_table = "product_images"
        verbose_name = "изображение товара"
        verbose_name_plural = "Изображения товара"

class ProductView(models.Model):
    product = models.ForeignKey(
        to=Product,
        on_delete=models.CASCADE,
        related_name='views',
        verbose_name="Продукт"
    )
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        null=True,
        blank=True
    )
    ip_address = models.GenericIPAddressField(verbose_name="IP адрес")
    date = models.DateTimeField(auto_now=True, verbose_name="Дата просмотра")
    
    class Meta:
        db_table="view"
        verbose_name="просмотр"
        verbose_name_plural="Просмотры"