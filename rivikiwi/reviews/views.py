from django.shortcuts import redirect, render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from reviews.forms import ReviewForm
from reviews.models import Review
from reviews.utils import seller_reviews
from users.models import User


def all_reviews(request, seller_username):
    reviews = seller_reviews(seller_username)

    context = {"reviews": reviews, "seller_username": seller_username}

    return render(request, "reviews/reviews.html", context)


@login_required
def create_review(request, seller_username):
    reviews = seller_reviews(seller_username)

    if request.method == "POST":
        seller = User.objects.get(username=seller_username)
        form = ReviewForm(data=request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.seller = seller
            review.consumer = request.user
            review.save()

        return redirect("reviews:all_reviews", seller_username=seller_username)
    else:
        form = ReviewForm()

    context = {"form": form, "seller_username": seller_username, "reviews": reviews}
    return render(request, "reviews/reviews.html", context)


@login_required
def edit_review(request):
    review_id = request.POST.get("review_id")
    review = get_object_or_404(Review, id=review_id)
    form_data = {
        "text" : request.POST.get("text"),
        "rating" : request.POST.get("rating")
    }
    form = ReviewForm(data=form_data, instance=review)

    if form.is_valid():
        form.save()

    return redirect("reviews:all_reviews", seller_username=review.seller)


@login_required
def delete_review(request):
    review_id = request.POST.get("review_id")
    review = Review.objects.get(id=review_id)
    review.delete()
    
    response_data = {
        "message" : "Отзыв успешно удален"
    }
    
    return JsonResponse(response_data)
