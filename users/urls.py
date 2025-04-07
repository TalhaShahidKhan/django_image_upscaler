from django.urls import path, include
from .views import CustomPasswordResetView, SignupView, CustomPasswordResetConfirmView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("password_reset/", CustomPasswordResetView.as_view(html_email_template_name="registration/password_reset_html_email.html"), name="password_reset"),
    path(
        "reset/<uidb64>/<token>/",
        CustomPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path("signup/", SignupView.as_view(), name="signup"),
    path("", include("django.contrib.auth.urls")),
]
app_name = "users"
