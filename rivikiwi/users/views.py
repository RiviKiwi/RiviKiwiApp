from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import UserAuthenticationForm, UserRegistrationForm
from django.contrib import auth


def login(request):
    if request.method == "POST":
        form = UserAuthenticationForm(data = request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                redirect_page = request.POST.get("next", None)
                if redirect_page and redirect_page != reverse('users:logout'):
                    return HttpResponseRedirect(redirect_page)
                
                return HttpResponseRedirect(reverse('catalog:home'))
    else:
        form = UserAuthenticationForm()
    context = {
        'form':form,
    }
    return render(request, 'users/login.html', context)


def registration(request):
    BACKEND = 'django.contrib.auth.backends.ModelBackend'
    if request.method == "POST":
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = form.instance
            auth.login(request, user, backend=BACKEND)
            return HttpResponseRedirect(reverse('catalog:home'))
    else:
        form = UserRegistrationForm()            
    context = {
        'form':form,
    }
    return render(request, 'users/registration.html', context)


def logout(request):
    auth.logout(request)
    return redirect(reverse('catalog:home'))