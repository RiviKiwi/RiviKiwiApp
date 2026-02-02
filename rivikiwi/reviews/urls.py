from django.urls import path
from reviews import views

app_name = 'reviews'

urlpatterns = [
    path('edit/', views.EditReviewView.as_view(), name='edit_review'),
    path('delete/', views.DeleteReviewView.as_view(), name='delete_review'),
    path('<str:seller_username>/', views.ReviewsView.as_view(), name='all_reviews'),
    path('<str:seller_username>/create/', views.CreateReviewView.as_view(), name='create_review'),
]