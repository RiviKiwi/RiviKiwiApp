from django.db import models
from rivikiwi import settings

class ReviewQuerySet(models.QuerySet):
    def avg_rating(self):
        return round(sum(review.rating for review in self) / len(self), 1)
    
    def reviews_count(self):
        return len(self)

class Review(models.Model):
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="seller",
        verbose_name="Продавец",
    )
    consumer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="consumer",
        verbose_name="Покупатель",
    )
    text = models.TextField(verbose_name="Отзыв")
    rating = models.IntegerField(
        choices=[(x, x) for x in range(1, 6)], verbose_name="Оценка"
    )
    
    objects = ReviewQuerySet.as_manager()

    class Meta:
        db_table = "reviews"
        verbose_name = "отзыв"
        verbose_name_plural = "отзывы"
        constraints = [
            models.UniqueConstraint(
                fields=["seller", "consumer"], name="unique_consumer_review"
            )
        ]
        
    def __str__(self):
        return f"Отзыв пользователя {self.consumer.username}"
