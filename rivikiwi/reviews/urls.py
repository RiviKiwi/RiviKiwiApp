from django.urls import path
from reviews import views

app_name = 'reviews'

urlpatterns = [
    path('reviews/<int:product_id>/', views.all_reviews, name='all_rewiews'),
    path('reviews/<int:product_id>/<int:review_id>/', views.single_review, name='single_review'),
    path('reviews/<int:product_id>/create/', views.create_review, name='create_review')
]