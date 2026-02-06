
from django.urls import path
from . import views

app_name = 'wishlist'

urlpatterns = [
    path('', views.WishlistView.as_view(), name="index"),
    path('add/<int:product_id>/', views.AddWishlistView.as_view(), name="add"),
    path('delete/<int:product_id>/', views.DeleteWishlistView.as_view(), name="delete"),
]
