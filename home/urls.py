from django.urls import path
from .views import DashboardView,CreditListNonUserView,ContactUsView,AboutUsView,htmx_contact_form_view
urlpatterns = [
    path('dashboard/',DashboardView.as_view(),name='dashboard'),
    path('pricing/',CreditListNonUserView.as_view(),name='pricing'),
    path('contact/',ContactUsView.as_view(),name='contact'),
    path('about/',AboutUsView.as_view(),name='about'),
    path('contact_form/',htmx_contact_form_view,name='cf'),
]

app_name="home"