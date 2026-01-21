from django import forms
from reviews.models import Review


class ReviewForm(forms.ModelForm):
    images = forms.FileField(widget=forms.ClearableFileInput(attrs={"multiple": True}))

    class Meta:
        model = Review
        fields = ["text", "rating"]
