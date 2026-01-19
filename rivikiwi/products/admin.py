from django.contrib import admin
from .models import ProductCategory, Product, ProductImage


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields  = {'slug':('name',)}
    list_display=['name', 'slug']
    search_fields=['name', 'slug']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields  = {'slug':('name',)}
    list_display=['name', 'slug', 'price', 'category']
    search_fields=['name', 'slug']
    
@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display=['id', 'image', 'is_main']
    search_fields=['id']