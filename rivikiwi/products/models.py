from django.db import models


class ProductCategory(models.Model):
    name = models.CharField(max_length=35, blank=True, null=True, unique=True, verbose_name="Название")
    slug = models.SlugField(unique=True, verbose_name="url")
    
    class Meta:
        db_table = 'product_category'
        verbose_name = 'категорию'
        verbose_name_plural = 'категории'
        
    
        
