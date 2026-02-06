from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib import auth
from django.views.generic import CreateView, DetailView
from .forms import UserAuthenticationForm, UserRegistrationForm, ProfileForm
from products.models import Product
from users.models import User


class UserLoginView(LoginView):
    template_name="users/login.html"
    form_class=UserAuthenticationForm
    # success_url = reverse_lazy('catalog:home')
    
    def get_success_url(self):
        redirect_page = self.request.POST.get("next", None)
        if redirect_page and redirect_page != reverse("users:logout"):
            return redirect_page
        return reverse_lazy("catalog:home")
    
    def form_valid(self, form):
        response = super().form_valid(form)
        
        return response

    def form_invalid(self, form):
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class UserRegistrationView(CreateView):
    template_name="users/registration.html"
    form_class=UserRegistrationForm
    success_url=reverse_lazy("catalog:home")
    BACKEND = "django.contrib.auth.backends.ModelBackend"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class SelfProfileView(LoginRequiredMixin, UpdateView):
    template_name = "users/self-profile.html"
    form_class = ProfileForm
    success_url = reverse_lazy("users:self_profile")
    

    def get_object(self, queryset=None):
        return self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_products = Product.objects.filter(user=self.request.user)
        context["user_products"]=user_products
        return context
        


class SellerProfileView(DetailView):
    template_name = "users/user-profile.html"
    context_object_name = "seller"
    
    def get_object(self, queryset = None):
        return User.objects.get(username=self.kwargs.get("username"))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        seller = self.kwargs.get('seller')
        seller_products = Product.objects.filter(user=seller)
        context["seller_products"]=seller_products
        return context