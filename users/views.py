from django.shortcuts import render
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django import forms
from django.contrib.auth import get_user_model
from django.views.generic import CreateView
from django.conf import settings
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm

User = get_user_model()
# Create your views here.
class CustomPasswordResetForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email"})
    )

    def clean_email(self):
        email = self.cleaned_data["email"]
        if not get_user_model().objects.filter(email=email).exists():
            raise ValidationError("There is no user registered with this email address.")
        return email

class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm




class SignupView(CreateView):
    model=User
    form_class = CustomUserCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy('users:login')
    
    def get_success_url(self):
        return settings.SIGNUP_REDIRECT_URL