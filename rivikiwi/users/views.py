import re
import logging
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import UpdateView
from django.contrib import auth
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView, DetailView
from .forms import UserAuthenticationForm, UserRegistrationForm, ProfileForm
from products.models import Product
from users.models import User

logger = logging.getLogger('users_app')


class UserLoginView(LoginView):
    template_name = "users/login.html"
    form_class = UserAuthenticationForm

    def get_success_url(self):
        redirect_page = self.request.POST.get("next", None)
        pattern = re.compile(r"^/wishlist/(add|delete)/\d+/$")
        
        logger.debug("Checking pattern of loging")
        
        if redirect_page and redirect_page != reverse("users:logout") and not pattern.match(redirect_page):
            logger.info(f"Redirecting to requested page: {redirect_page}")
            return redirect_page
        
        logger.info("Redirect to main page")
        return reverse_lazy("catalog:home")

    def form_valid(self, form):
        response = super().form_valid(form)
        logger.info("User data is correct in login form")
        
        return response

    def form_invalid(self, form):
        logger.warning("User data is not correct in login form")
        
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        logger.warning("Context is created successfully for login")
        
        return context


class UserRegistrationView(CreateView):
    template_name = "users/registration.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy("catalog:home")
    BACKEND = "django.contrib.auth.backends.ModelBackend"
    
    def form_valid(self, form):
        logger.debug("Start checking registration form")
        user = form.instance
        logger.info("Get user in registration form")
        
        if user:
            form.save()
            logger.info("Correct registration form")
            
            auth.login(self.request, user, backend=self.BACKEND)
            logger.warning("User authenticated successfully")
            
        return HttpResponseRedirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        logger.warning("Context is created successfully for registration")
        return context


class SelfProfileView(LoginRequiredMixin, UpdateView):
    template_name = "users/self-profile.html"
    form_class = ProfileForm
    success_url = reverse_lazy("users:self_profile")

    def get_object(self, queryset=None):
        logger.debug("Get user in self profile")
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        logger.debug("Get default context in user profile")
        
        user_products = Product.objects.filter(user=self.request.user)
        logger.info("Get all products which have user")
        
        context["user_products"] = user_products
        logger.warning("Context is created successfully for user profile")
        return context


class SellerProfileView(DetailView):
    template_name = "users/user-profile.html"
    context_object_name = "seller"

    def get_object(self, queryset=None):
        logger.debug("Get user in seller profile")
        return User.objects.get(username=self.kwargs.get("username"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        logger.debug("Get default context in seller profile")
        
        seller = self.get_object()
        logger.info("Get seller")
        
        seller_products = Product.objects.filter(user=seller)
        logger.info("Get all products which have seller")
        
        context["seller_products"] = seller_products
        logger.warning("Context is created successfully for seller profile")
        
        return context
