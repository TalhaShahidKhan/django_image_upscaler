from django.urls import path
from .views import ListCreditsView, create_dynamic_transaction, payment_success,webhook

urlpatterns = [
    path('credits/', ListCreditsView.as_view(), name='list_credits'),
    path('pay/<int:credit_id>/', create_dynamic_transaction, name="transaction"),
    path('success/', payment_success, name="payment_success"),
    path('webhook/', webhook, name="webhook"),
]

app_name = "payments"