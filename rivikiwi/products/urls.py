
from django.urls import path
from products import views

app_name = 'products'

urlpatterns = [
    path('', views.IndexView.as_view(), name="home"),
    path('search/', views.IndexView.as_view(), name="search"),
    path('add_product/', views.AddProductView.as_view(), name="add_product"),
    path('edit_product/<slug:product_slug>/', views.EditProductView.as_view(), name="edit_product"),
    path('delete_product/<slug:product_slug>/', views.DeleteProductView.as_view(), name="delete_product"),
    path('<slug:category_slug>/', views.IndexView.as_view(), name="index"),
    path('product/<slug:product_slug>/', views.ProductViewController.as_view(), name="product")

]
