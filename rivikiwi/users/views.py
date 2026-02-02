from django.urls import reverse, reverse_lazy
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from .forms import UserAuthenticationForm, UserRegistrationForm, ProfileForm
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


class UserProfileView(LoginRequiredMixin, UpdateView):
    template_name = "users/self-profile.html"
    form_class = ProfileForm

    def get_object(self, queryset=None):
        return self.request.user

    def is_self_profile(self):
        user = self.get_object()
        return user.username == self.kwargs.get("username")

    def get_success_url(self):
        return reverse_lazy(
            "users:profile", kwargs={"username": self.kwargs.get("username")}
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.is_self_profile():
            self.template_name = "users/user-profile.html"
            context["seller"] = User.objects.get(username=self.kwargs.get("username"))
        return context
