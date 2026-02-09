from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from reviews.models import Review

class User(AbstractUser):
    middle_name = models.CharField(max_length=30, blank=True, null=True, verbose_name="Отчество")
    phone = PhoneNumberField(blank=True, null=True, unique=True, region='BY', verbose_name="Номер телефона")
    profile_description = models.TextField(blank=True, null=True, verbose_name="Описание профиля")
    avatar = models.ImageField(upload_to="users_images", blank=True, null=True, verbose_name="Аватар")
    email = models.EmailField(unique=True, verbose_name="Почта")
    
    class Meta:
        db_table = "user"
        verbose_name = "Пользователю"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"{self.username}"
    
    def get_fullname(self):
        default_name = f"{self.first_name} {self.last_name}"
        return default_name + f" {self.middle_name}" if self.middle_name else default_name
    
    def get_rating(self):
        reviews = Review.objects.filter(seller=self)
        return reviews.avg_rating()

        
    