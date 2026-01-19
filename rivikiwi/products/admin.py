from django.contrib import admin
from .models import ProductCategory


@admin.register(ProductCategory)
class CarBrandAdmin(admin.ModelAdmin):
    prepopulated_fields  = {'slug':('name',)}
    list_display=['name', 'slug']
    search_fields=['name', 'slug']



