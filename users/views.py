from django.shortcuts import render
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django import forms

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
