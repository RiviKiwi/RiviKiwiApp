from django.contrib import admin
from reviews.models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display=['id', 'text', 'seller', 'consumer', 'rating']
    search_fields=['id']
    