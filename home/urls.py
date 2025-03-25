from django.urls import path
from .views import DashboardView
urlpatterns = [
    path('dashboard/',DashboardView.as_view(),name='dashboard')
]

app_name="home"