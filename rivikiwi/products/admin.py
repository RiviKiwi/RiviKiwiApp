from django.contrib import admin
from .models import ProductCategory, Product, ProductImage


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields  = {'slug':('name',)}
    list_display=['name', 'slug']
    search_fields=['name', 'slug']




