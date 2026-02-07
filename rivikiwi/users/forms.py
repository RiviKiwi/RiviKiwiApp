from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django import forms
from .models import User
from captcha.fields import CaptchaField
import re

class UserAuthenticationForm(AuthenticationForm):
    username=forms.CharField()
    password=forms.CharField()
    class Meta:
        model = User
        fields = ['username', 'password']
        
    # def clean_username(self):
    #     data = self.cleaned_data['username']
        
    #     pattern = re.compile(r'^\w{5,30}$')
        
    #     if not pattern.match(data):
    #         raise forms.ValidationError("Неверный формат username")

    #     return data
    
class UserRegistrationForm(UserCreationForm):
    username=forms.CharField()
    first_name=forms.CharField()
    middle_name=forms.CharField()
    last_name=forms.CharField()
    phone=forms.CharField()
    email=forms.CharField()
    password1=forms.CharField()
    password2=forms.CharField()
    captcha = CaptchaField()
    class Meta:
        model=User
        fields = [
            'username',
            'first_name',
            'middle_name',
            'last_name',
            'phone',
            'email',
            'password1',
            'password2'
        ]


class ProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = (
            "avatar", 
            "first_name",
            "last_name",
            "middle_name",
            "username",
            "phone", 
            "email",
            "profile_description"
            )

    avatar = forms.ImageField(required=False)
    first_name = forms.CharField()
    last_name = forms.CharField()
    middle_name = forms.CharField()
    username = forms.CharField()
    phone=forms.CharField()
    email = forms.CharField()
    profile_description = forms.CharField(required=False)
