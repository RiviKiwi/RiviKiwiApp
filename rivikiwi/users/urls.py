
from django.urls import path, reverse_lazy
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.login, name="login"),
    path('registration/', views.registration, name="registration"),
    path('profile/<str:username>', views.profile, name="profile"),
    path('logout/', views.logout, name="logout"),
    path('password_change/', PasswordChangeView.as_view(template_name="users/password_change.html",
                                                        success_url=reverse_lazy("users:password_change_done")), name='password_change'),
    path('password_change/done/', PasswordChangeDoneView.as_view(template_name="users/password_change_done.html"), name='password_change_done'),
]
