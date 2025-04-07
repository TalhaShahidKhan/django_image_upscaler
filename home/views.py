from typing import Any
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import redirect,render
from django.views.generic import TemplateView,ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from dj_cloudinary.models import Image
from payments.models import Credit
from home.models import ContactFormFeedback
# Create your views here.


class HomePageView(TemplateView):
    template_name='main.html'
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.user.is_authenticated:
            return redirect('/home/dashboard/')
        return super().get(request, *args, **kwargs)

class DashboardView(LoginRequiredMixin, ListView):
    model=Image
    login_url = '/users/login/'
    redirect_field_name = 'next'
    template_name = 'home/dashboard.html'
    context_object_name = "images"
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["images"] = Image.objects.filter(user=self.request.user).all()
        return context
    

class CreditListNonUserView(ListView):
    model = Credit
    template_name = "home/credit_list.html"
    context_object_name = "credits"
    


class ContactUsView(TemplateView):
    template_name="home/contact.html"


class AboutUsView(TemplateView):
    template_name="home/about.html"


def htmx_contact_form_view(request):
    """Handle HTMX form submission for contact form"""
    if request.method == "POST":
        email = request.POST.get('email', '')
        message = request.POST.get('message', '')
        subject = request.POST.get('subject', 'General Inquiry')
        name = request.POST.get('name', '')
        
        # Combine name and subject with message for better context
        feedback_text = f"From: {name}\nSubject: {subject}\n\nMessage:\n{message}"
        
        # Create and save the feedback
        if email and message:
            feedback = ContactFormFeedback(
                email=email,
                feedback=feedback_text
            )
            feedback.save()
            
            # Return successful response for HTMX
            return HttpResponse("""
                <div class="p-4 mb-4 text-sm text-green-800 rounded-lg bg-green-50 dark:bg-gray-800 dark:text-green-400" role="alert">
                    <div class="flex items-center">
                        <svg class="w-4 h-4 me-2 flex-shrink-0" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
                            <path d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5Zm3.707 8.207-4 4a1 1 0 0 1-1.414 0l-2-2a1 1 0 0 1 1.414-1.414L9 10.586l3.293-3.293a1 1 0 0 1 1.414 1.414Z"/>
                        </svg>
                        <span class="font-medium">Thank you for your message!</span>
                    </div>
                    <div class="mt-2">
                        We've received your feedback and will get back to you soon.
                    </div>
                </div>
            """)
        else:
            # Return error response for HTMX
            return HttpResponse("""
                <div class="p-4 mb-4 text-sm text-red-800 rounded-lg bg-red-50 dark:bg-gray-800 dark:text-red-400" role="alert">
                    <div class="flex items-center">
                        <svg class="w-4 h-4 me-2 flex-shrink-0" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
                            <path d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5Zm3.707 8.207-4 4a1 1 0 0 1-1.414 0l-2-2a1 1 0 0 1 1.414-1.414L9 10.586l3.293-3.293a1 1 0 0 1 1.414 1.414Z"/>
                        </svg>
                        <span class="font-medium">Please provide both email and message!</span>
                    </div>
                </div>
            """)
    
    # For non-POST requests, return an empty response
    return HttpResponse("")