from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, View
from django.core.cache import cache
from django.contrib.auth.mixins import LoginRequiredMixin
from reviews.forms import ReviewForm
from reviews.models import Review
from reviews.utils import seller_reviews
from users.models import User


class ReviewsView(ListView):
    model = Review
    template_name = "reviews/reviews.html"
    context_object_name = "reviews"

    def get_queryset(self):
        seller_username = self.kwargs.get("seller_username")
        reviews = cache.get("reviews")
        if not reviews:
            reviews = seller_reviews(seller_username)
            cache.set("reviews", reviews, 10*60)
        return reviews

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["seller_username"] = self.kwargs.get("seller_username")
        return context


class CreateReviewView(LoginRequiredMixin, CreateView):
    template_name = "reviews/reviews.html"
    form_class = ReviewForm

    def get_seller_username(self):
        return self.kwargs.get("seller_username")

    def get_success_url(self):
        seller_username = self.get_seller_username()
        return reverse_lazy(
            "reviews:all_reviews", kwargs={"seller_username": seller_username}
        )

    def form_valid(self, form):
        seller = User.objects.get(username=self.get_seller_username())
        review = form.save(commit=False)
        review.seller = seller
        review.consumer = self.request.user
        review.save()
        
        cache_data = cache.get("reviews")
        if cache_data:
            cache.delete("reviews")
            
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        seller_username = self.get_seller_username()
        context["seller_username"] = seller_username
        context["reviews"] = seller_reviews(seller_username)
        return context


class EditReviewView(LoginRequiredMixin, UpdateView):
    template_name = "reviews/reviews.html"
    form_class = ReviewForm

    def get_object(self, queryset=None):
        review_id = self.request.POST.get("review_id")
        cache_data = cache.get("reviews")
        if cache_data:
            cache.delete("reviews")
        return Review.objects.get(id=review_id)

    def get_initial(self):
        initial = super().get_initial()
        initial["text"] = self.request.POST.get("text")
        initial["rating"] = self.request.POST.get("rating")
        return initial

    def get_success_url(self):
        review = self.get_object()
        return reverse_lazy(
            "reviews:all_reviews", kwargs={"seller_username": review.seller}
        )


class DeleteReviewView(LoginRequiredMixin, View):
    def post(self, request):
        review_id = request.POST.get("review_id")
        review = Review.objects.get(id=review_id)
        review.delete()
        
        cache_data = cache.get("reviews")
        if cache_data:
            cache.delete("reviews")

        response_data = {"message": "Отзыв успешно удален"}

        return JsonResponse(response_data)
