from django.contrib import admin
from reviews.models import Review, ReviewImage


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display=['id', 'text']
    search_fields=['id']

@admin.register(ReviewImage)
class ReviewImageAdmin(admin.ModelAdmin):
    list_display=['id', 'image']
    search_fields=['id']
    