from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserAuthenticationForm, UserRegistrationForm, ProfileForm
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from users.models import User


def login(request):
    if request.method == "POST":
        form = UserAuthenticationForm(data=request.POST)
        if form.is_valid():
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                redirect_page = request.POST.get("next", None)
                if redirect_page and redirect_page != reverse("users:logout"):
                    return HttpResponseRedirect(redirect_page)

                return HttpResponseRedirect(reverse("catalog:home"))
    else:
        form = UserAuthenticationForm()
    context = {
        "form": form,
    }
    return render(request, "users/login.html", context)

def registration(request):
    BACKEND = "django.contrib.auth.backends.ModelBackend"
    if request.method == "POST":
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = form.instance
            auth.login(request, user, backend=BACKEND)
            return HttpResponseRedirect(reverse("catalog:home"))
    else:
        form = UserRegistrationForm()
    context = {
        "form": form,
    }
    return render(request, "users/registration.html", context)

class UserProfileView(LoginRequiredMixin, UpdateView):
    form_class = ProfileForm
    template_name = 'users/self-profile.html'
    
    def is_self_profile(self):
        return self.request.user.username == self.kwargs.get('username')
    
    def get_object(self, queryset=None):
        return self.request.user
    
    def get(self, request, *args, **kwargs):
        if not self.is_self_profile():
            seller = User.objects.get(username=self.kwargs.get('username'))
            self.template_name = 'users/user-profile.html'
            context = {'seller': seller}
            return self.render_to_response(context)
            
        return super().get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        if not self.is_self_profile():
            return redirect('users:profile', username=self.kwargs.get('username'))
            
        return super().post(request, *args, **kwargs)
    
    
    def get_success_url(self):
        return reverse_lazy('users:profile', kwargs={'username': self.kwargs.get('username')})

@login_required
def logout(request):
    auth.logout(request)
    return redirect(reverse("catalog:home"))


