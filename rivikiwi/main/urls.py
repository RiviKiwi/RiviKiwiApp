
from django.urls import path
from main import views

app_name = 'main'

urlpatterns = [
    path('about/',views.AboutView.as_view(), name="about"),
]
