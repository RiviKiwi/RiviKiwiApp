
from django.urls import path
from . import views

app_name = 'wishlist'

urlpatterns = [
    path('', views.WishlistView.as_view(), name="index"),
    path('work_with_wishlist/<int:product_id>/', views.WorkWithWishlistView.as_view(), name="add"),
]
