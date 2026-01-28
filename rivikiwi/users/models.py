from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

class User(AbstractUser):
    middle_name = models.CharField(max_length=30, blank=True, null=True, verbose_name="Отчество")
    phone = PhoneNumberField(blank=True, region='BY', verbose_name="Номер телефона")
    class Meta:
        db_table = "user"
        verbose_name = "Пользователю"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"{self.username}"
    
    def get_fullname(self):
        return f"{self.first_name} {self.last_name} {self.middle_name}"
    