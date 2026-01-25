
from django.urls import path
from products import views

app_name = 'products'

urlpatterns = [
    path('<slug:category_slug>/', views.index, name="index"),
    path('product/<slug:product_slug>/', views.product, name="product")
]
