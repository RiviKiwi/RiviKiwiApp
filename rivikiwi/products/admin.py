from django.contrib import admin
from .models import ProductCategory, Product, ProductImage, ProductView, City


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields  = {'slug':('name',)}
    list_display=['name', 'slug']
    search_fields=['name', 'slug']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields  = {'slug':('name',)}
    list_display=['name', 'slug', 'price', 'category', 'creation_date']
    search_fields=['name', 'slug']
    
@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display=['id', 'image', 'is_main']
    search_fields=['id']
    
@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
    list_display=['id', 'name', 'slug']
    search_fields=['id', 'name', 'slug']
    
@admin.register(ProductView)
class ProductViewAdmin(admin.ModelAdmin):
    list_display=['id', 'user', 'product','ip_address']
    search_fields=['id', 'user', 'product','ip_address']