from django.urls import path, include
from .views import CustomPasswordResetView,SignupView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('', include('django.contrib.auth.urls')),
]
app_name='users'