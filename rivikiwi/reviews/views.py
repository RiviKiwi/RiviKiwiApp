import logging
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, CreateView, UpdateView, View
from django.core.cache import cache
from django.contrib.auth.mixins import LoginRequiredMixin
from reviews.forms import ReviewForm
from reviews.models import Review
from reviews.utils import seller_reviews
from users.models import User

logger = logging.getLogger("reviews_app")


class ReviewsView(ListView):
    model = Review
    template_name = "reviews/reviews.html"
    context_object_name = "reviews"

    def get_queryset(self):
        seller_username = self.kwargs.get("seller_username")
        logger.debug("Get seller username")
        reviews = cache.get("reviews")
        logger.debug("Get reviews from cache")
        if not reviews:
            reviews = seller_reviews(seller_username)
            logger.debug("Get seller reviews by seller username")
            cache.set("reviews", reviews, 10 * 60)
            logger.debug("Set cache for seller reviews")
        logger.info("Reviews ready to set in context")
        return reviews

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        logger.debug("Get context")
        context["seller_username"] = self.kwargs.get("seller_username")
        logger.debug("Set seller username to context")
        logger.info("Context ready for rendering page")
        return context


class CreateReviewView(LoginRequiredMixin, CreateView):
    template_name = "reviews/reviews.html"
    form_class = ReviewForm

    def get_seller_username(self):
        logger.info("Return seller username")
        return self.kwargs.get("seller_username")

    def get_success_url(self):
        seller_username = self.get_seller_username()
        logger.debug("Get seller username")
        logger.info("Return success url and pass seller username to page url")
        return reverse_lazy(
            "reviews:all_reviews", kwargs={"seller_username": seller_username}
        )

    def form_valid(self, form):
        seller = User.objects.get(username=self.get_seller_username())
        logger.debug("Get seller object")
        review = form.save(commit=False)
        logger.debug("Create review object, but dont save it to DB")
        review.seller = seller
        logger.debug("Set seller to review")
        review.consumer = self.request.user
        logger.debug("Set customer to review")
        review.write_date = timezone.now()
        logger.debug("Set write date to review")
        review.save()
        logger.debug("Save review in DB")

        cache_data = cache.get("reviews")
        logger.debug("Get reviews cache")
        if cache_data:
            cache.delete("reviews")
            logger.debug("Successfuly delete cache for reviews")

        logger.info("Redirecting to success url")
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        logger.debug("Get context")
        seller_username = self.get_seller_username()
        context["seller_username"] = seller_username
        logger.debug("Set seller username to context")
        context["reviews"] = seller_reviews(seller_username)
        logger.debug("Set reviews to context")
        logger.info("Context ready for rendering page")
        return context


class EditReviewView(LoginRequiredMixin, UpdateView):
    template_name = "reviews/reviews.html"
    form_class = ReviewForm

    def get_object(self, queryset=None):
        review_id = self.request.POST.get("review_id")
        logger.debug("Get review id from POST request")
        cache_data = cache.get("reviews")
        logger.debug("Get reviews cache")
        if cache_data:
            cache.delete("reviews")
            logger.debug("Successfuly delete reviews cache")

        review = Review.objects.get(id=review_id)
        logger.debug("Get review object by id")
        review.write_date = timezone.now()
        logger.debug("Update write date to current")
        logger.info("Review is ready to context")
        return review

    def get_initial(self):
        initial = super().get_initial()
        initial["text"] = self.request.POST.get("text")
        logger.debug("Set text into initial form data")
        initial["rating"] = self.request.POST.get("rating")
        logger.debug("Set rating into initial form data")
        logger.info("Initial data is ready to form")
        return initial

    def get_success_url(self):
        review = self.get_object()
        logger.debug("Get review object")
        logger.info("Redirect to success page and pass review seller to it")
        return reverse_lazy(
            "reviews:all_reviews", kwargs={"seller_username": review.seller}
        )


class DeleteReviewView(LoginRequiredMixin, View):
    def post(self, request):
        review_id = request.POST.get("review_id")
        logger.debug("Get review id from POST request")
        review = Review.objects.get(id=review_id)
        logger.debug("Get review object by id from DB")
        review.delete()
        logger.debug("Succesfully delete review")

        cache_data = cache.get("reviews")
        if cache_data:
            cache.delete("reviews")

        logger.debug("Update cache")

        response_data = {"message": "Отзыв успешно удален"}
        logger.info("Make ajax request to delete review smoothly")
        return JsonResponse(response_data)
