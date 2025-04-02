from typing import Any
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import redirect
from django.views.generic import TemplateView,ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from dj_cloudinary.models import Image
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
    