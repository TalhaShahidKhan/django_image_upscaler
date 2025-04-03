from typing import Any
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from .models import Credit,Payment
from django.contrib.auth import get_user_model
import json
import hmac
import hashlib
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.shortcuts import render
from django.urls import reverse_lazy
from django.db import transaction

User = get_user_model()

class ListCreditsView(LoginRequiredMixin,ListView):
    model = Credit
    template_name = "payments/list_credits.html"
    context_object_name = "credits" 
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["paddle_client_side_token"] = settings.PADDLE_CLIENT_SIDE_TOKEN
        return context

@csrf_exempt
@require_POST
def paddle_webhook(request):
    # Verify the webhook signature (replace with your Paddle secret)
    payload = request.POST.copy()
    signature = payload.pop('p_signature', None)
    
    # Sort payload alphabetically and serialize
    serialized = '&'.join(f'{k}={v}' for k, v in sorted(payload.items()))
    
    # Verify with your webhook secret (from Paddle dashboard)
    # This is different from your client side token
    computed_signature = hmac.new(
        settings.PADDLE_WEBHOOK_SECRET.encode('utf-8'),
        serialized.encode('utf-8'),
        hashlib.sha1
    ).hexdigest()
    
    if signature != computed_signature:
        return HttpResponse(status=400)
    
    # Handle the webhook events
    event = payload.get('alert_name')
    
    if event == 'payment_succeeded':
        # Get user and credit details
        checkout_id = payload.get('checkout_id')
        product_id = payload.get('product_id')
        email = payload.get('email')
        
        # Check if this checkout was already processed
        if Payment.objects.filter(checkout_id=checkout_id).exists():
            # Already processed, just return success
            return HttpResponse(status=200)
        
        # Find the user and credit package
        try:
            user = User.objects.get(email=email)
            credit = Credit.objects.get(product_id=product_id)
        except (User.DoesNotExist, Credit.DoesNotExist):
            # Log error but don't return error status to Paddle
            # This prevents Paddle from retrying failed webhooks
            return HttpResponse(status=200)
        
        # Create the payment record with checkout_id
        payment = Payment.objects.create(
            user=user,
            credit=credit,
            checkout_id=checkout_id,
            amount=credit.price
        )
        
        # Add credits to user's account
        user.upscale_credit += credit.number_of_credits
        user.save()
    
    return HttpResponse(status=200)

@require_POST
def complete_purchase(request):
    try:
        data = json.loads(request.body)
        checkout_id = data.get('checkout_id')
        product_id = data.get('product_id')
        
        # Check if this checkout was already processed
        if Payment.objects.filter(checkout_id=checkout_id).exists():
            return JsonResponse({'status': 'already_processed'})
        
        # Get credit and user
        try:
            credit = Credit.objects.get(product_id=product_id)
        except Credit.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Invalid product'}, status=400)
        
        user = request.user
        
        # Use a transaction to ensure atomicity
        with transaction.atomic():
            # Create payment record
            payment = Payment.objects.create(
                user=user,
                credit=credit,
                checkout_id=checkout_id  
            )
            
            # Add credits to user's account
            user.upscale_credit += credit.number_of_credits
            user.save()
        
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

def payment_success(request):
    # Show a success page
    return render(request, 'payments/success.html')