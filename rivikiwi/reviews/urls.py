from django.urls import path
from reviews import views

app_name = 'reviews'

urlpatterns = [
    path('<str:seller_username>/', views.all_reviews, name='all_reviews'),
    path('<str:seller_username>/<int:review_id>/', views.single_review, name='single_review'),
    path('<str:seller_username>/create/', views.create_review, name='create_review'),
    path('<int:review_id>/edit/', views.edit_review, name='edit_review'),
    path('<int:review_id>/delete/', views.delete_review, name='delete_review'),
]