from django.urls import path
from .views import ListCreditsView, paddle_webhook, complete_purchase, payment_success

urlpatterns = [
    path('credits/', ListCreditsView.as_view(), name='list_credits'),
    path('webhook/', paddle_webhook, name='webhook'),
    path('complete/', complete_purchase, name='complete'),
    path('success/', payment_success, name='success'),
]

app_name = "payments"