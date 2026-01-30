from django import forms
from .models import Product
from multiupload.fields import MultiFileField    

class AddProductForm(forms.ModelForm):
    name = forms.CharField()
    category = forms.CharField()
    description=forms.CharField()
    images = MultiFileField(min_num=0, max_num=10, required=False)
    price = forms.CharField()
    discount = forms.CharField()
    city = forms.CharField()
    
    class Meta:
        model = Product
        fields=[
                "name",
                "description",
                "price",
                "discount"
                ]