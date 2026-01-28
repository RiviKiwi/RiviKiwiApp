from reviews.models import Review


def seller_reviews(seller_username):
    return Review.objects.filter(seller__username=seller_username)
