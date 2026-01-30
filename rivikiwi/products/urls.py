
from django.urls import path
from products import views

app_name = 'products'

urlpatterns = [
    path('', views.index, name="home"),
    path('search/', views.index, name="search"),
    path('add_product/', views.add_product, name="add_product"),
    path('<slug:category_slug>/', views.index, name="index"),
    path('product/<slug:product_slug>/', views.product, name="product")
]
