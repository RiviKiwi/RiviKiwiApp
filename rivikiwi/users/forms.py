from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django import forms
from .models import User

class UserAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']
    
class UserRegistrationForm(UserCreationForm):
    username=forms.CharField()
    first_name=forms.CharField()
    middle_name=forms.CharField()
    last_name=forms.CharField()
    phone=forms.CharField()
    email=forms.CharField()
    password1=forms.CharField()
    password2=forms.CharField()
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
            "email"
            )

    avatar = forms.ImageField(required=False)
    first_name = forms.CharField()
    last_name = forms.CharField()
    middle_name = forms.CharField()
    username = forms.CharField()
    phone=forms.CharField()
    email = forms.CharField()
