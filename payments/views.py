from typing import Any
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from .models import Credit, Payment
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.shortcuts import render
from paddle_billing import Client, Environment, Options
from paddle_billing.Entities.Shared.TaxCategory import TaxCategory
from paddle_billing.Resources.Transactions.TransactionsClient import CreateTransaction
from paddle_billing.Resources.Transactions.Operations.Create import (
    TransactionCreateItemWithPrice,
)
from paddle_billing.Resources.Transactions.Operations.Price import (
    TransactionNonCatalogPriceWithProduct,
)
from paddle_billing.Entities.Shared.Money import Money
from paddle_billing.Entities.Shared.CurrencyCode import CurrencyCode
from paddle_billing.Resources.Transactions.Operations.Price.TransactionNonCatalogProduct import (
    TransactionNonCatalogProduct,
)
from django.db import transaction


User = get_user_model()


class ListCreditsView(LoginRequiredMixin, ListView):
    model = Credit
    template_name = "payments/list_credits.html"
    context_object_name = "credits"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["paddle_client_side_token"] = settings.PADDLE_CLIENT_SIDE_TOKEN.strip()
        context["paddle_env"] = settings.PADDLE_ENVIRONMENT.strip()
        return context


@require_POST
def create_dynamic_transaction(request, credit_id):
    try:
        credit = Credit.objects.get(id=credit_id)

        # Handle environment properly
        if settings.PADDLE_ENVIRONMENT.strip().lower() == "sandbox":
            env = Environment.SANDBOX
        else:
            env = Environment.PRODUCTION

        paddle = Client(
            settings.PADDLE_API_SECRET_KEY, options=Options(env)
        )

        # Create the transaction with more complete information
        transaction = paddle.transactions.create(
            CreateTransaction(
                items=[
                    TransactionCreateItemWithPrice(
                        price=TransactionNonCatalogPriceWithProduct(
                            name=f"{credit.price}$ amount of Credits",
                            description=f"Purchase of {credit.number_of_credits} credits",
                            unit_price=Money(
                                amount=str(
                                    int(credit.price * 100)
                                ),  # Ensure integer in cents
                                currency_code=CurrencyCode(value="USD"),
                            ),
                            product=TransactionNonCatalogProduct(
                                name=f"{credit.number_of_credits} Credits",
                                description=f"Package of {credit.number_of_credits} upscale credits",
                                tax_category=TaxCategory(value="saas"),
                            ),
                        ),
                        quantity=1,
                    )
                ],
                custom_data={"credit_id": str(credit.id), "user_email": request.user.email}
            )
        )

        print(f"Transaction created successfully: {transaction.id}")
        return JsonResponse({"msg": "success", "tnx_id": transaction.id}, status=200)

    except Exception as e:
        print(f"Paddle transaction error: {type(e).__name__}: {str(e)}")
        return JsonResponse({"msg": "There is an Error", "data": str(e)}, status=400)


def payment_success(request):
    """View to handle successful payments"""
    return render(request, "payments/success.html")


@csrf_exempt
@require_POST
def webhook(request):
    try:
        # 1. Verify webhook signature
        # integrity_check = Verifier(10).verify(
        #     request, Secret(settings.PADDLE_WEBHOOK_SECRET)
        # )
        # if not integrity_check:
        #     return JsonResponse({"message": "Invalid webhook signature"}, status=401)
        
        import json
        payload = json.loads(request.body)
        print(payload)
        event_type = payload.get('event_type')
        
        # 3. Only process transaction.completed events
        if event_type != 'transaction.completed':
            return JsonResponse({"message": f"Event type {event_type} ignored"}, status=200)
        
        # 4. Extract transaction data safely
        data = payload.get('data')
        print(data)
        custom_data = data.get('custom_data')
        print(custom_data)
        credit_id = custom_data.get('credit_id')
        customer_email = custom_data.get('user_email')
        
        if not credit_id or not customer_email:
            return JsonResponse({"message": "Missing credit_id or customer email"}, status=400)
        
        # 5. Find the user by email from the webhook data, not from request
        try:
            user = User.objects.get(email=customer_email)
        except User.DoesNotExist:
            return JsonResponse({"message": f"User with email {customer_email} not found"}, status=404)
        
        # 6. Get the credit information
        try:
            credit = Credit.objects.get(id=int(credit_id))
        except (Credit.DoesNotExist, ValueError):
            return JsonResponse({"message": f"Credit with ID {credit_id} not found"}, status=404)
        
        # 7. Create payment record
        payment = Payment.objects.create(
            user=user,
            credit=credit,  # Pass the credit object, not the ID
            amount=credit.price,
        )
        
        # 8. Update user credits
        user.upscale_credit += credit.number_of_credits
        user.save()
        
        # 9. Send email notification (consider making this asynchronous)
        try:
            send_mail(
                "Payment Successful",
                f"Your payment of ${credit.price} for {credit.number_of_credits} credits has been successful. "
                f"Credits have been added to your account.",
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=True,  # Changed to True so webhook doesn't fail if email fails
            )
        except Exception as e:
            print(f"Failed to send email: {str(e)}")
            # Don't return error, continue processing
        
        # 10. Return success
        return JsonResponse({"message": "Payment processed successfully"}, status=200)
    
    except Exception as e:
        import traceback
        print(f"Webhook error: {str(e)}")
        print(traceback.format_exc())
        # Still return 200 to acknowledge receipt (prevents Paddle from retrying repeatedly)
        return JsonResponse({"message": "Error processing webhook", "error": str(e)}, status=400)
