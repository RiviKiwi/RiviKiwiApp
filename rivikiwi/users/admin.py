from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display=['id', 'username', 'phone', 'email']
    search_fields=['id', 'username', 'phone', 'email']