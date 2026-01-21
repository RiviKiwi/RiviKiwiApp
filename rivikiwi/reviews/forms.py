from django import forms
from reviews.models import Review
from multiupload.fields import MultiFileField

class ReviewForm(forms.ModelForm):

    images = MultiFileField(min_num=0, max_num=10, required=False)

    class Meta:
        model = Review
        fields = ["text", "rating"]
