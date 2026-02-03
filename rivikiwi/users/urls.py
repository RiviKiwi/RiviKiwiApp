
from django.urls import path, reverse_lazy
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name="login"),
    path('registration/', views.UserRegistrationView.as_view(), name="registration"),
    path('profile/me', views.SelfProfileView.as_view(), name="self_profile"),
    path('profile/<str:username>', views.SellerProfileView.as_view(), name="seller_profile"),
    path('logout/', LogoutView.as_view(next_page="catalog:home"), name="logout"),
    path('password-change/', PasswordChangeView.as_view(template_name="users/password_change.html",
                                                        success_url=reverse_lazy("users:password_change_done")), name='password_change'),
    path('password-change/done/', PasswordChangeDoneView.as_view(template_name="users/password_change_done.html"), name='password_change_done'),
    path('password-reset/',
         PasswordResetView.as_view(
             template_name="users/password_reset_form.html",
             email_template_name="users/password_reset_email.html",
             extra_email_context={'encoding': '8bit'},
             success_url=reverse_lazy("users:password_reset_done")
         ),
         name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name="users/password_reset_done.html"), name="password_reset_done"),
    path('password-reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(
             template_name="users/password_reset_confirm.html",
             success_url=reverse_lazy("users:password_reset_complete")
         ),
         name='password_reset_confirm'),
    path('password-reset/complete/', PasswordResetCompleteView.as_view(template_name="users/password_reset_confirm_done.html"), name='password_reset_complete')
]
