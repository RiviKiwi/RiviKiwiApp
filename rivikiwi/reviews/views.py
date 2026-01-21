from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from reviews.forms import ReviewForm
from reviews.models import Review, ReviewImage


def all_reviews(request, product_id):
    reviews = Review.objects.filter(product=product_id)

    context = {"reviews": reviews}

    return render(request, "review/all_reviews.html", context)


def single_review(request, product_id, review_id):
    review = Review.objects.filter(id=review_id)

    context = {"review": review}

    return render(request, "reviews/singe_review.html", context)


@login_required
def create_review(request, product_id):
    if request.method == "POST":
        form = ReviewForm(data=request.POST)
        images = request.FILES.getlist("images")
        if len(images) > 6:
            images = images[::6]
            
        if form.is_valid():
            review = form.save(commit=False)
            review.product_id = product_id
            review.user = request.user
            review.save()

            for image in images:
                ReviewImage.objects.create(review=review, image=image)
        return HttpResponseRedirect(reverse("reviews:all_reviews"))
    else:
        form = ReviewForm()

    context = {"form": form}
    return render(request, "reviews/create_review.html", context)
