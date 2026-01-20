from django.db import models
from rivikiwi import settings


class Review(models.Model):
    user = settings.AUTH_USER_MODEL
    text = models.TextField(verbose_name="Отзыв")

    class Meta:
        db_table = "reviews"
        verbose_name = "отзыв"
        verbose_name_plural = "отзывы"


class ReviewImage(models.Model):
    review = models.ForeignKey(
        to=Review, on_delete=models.CASCADE, verbose_name="Отзыв"
    )
    image = models.ImageField(upload_to="reviews_images", verbose_name="Изображение")
