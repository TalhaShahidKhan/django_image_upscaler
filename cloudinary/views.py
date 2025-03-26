from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin


class ImageUpscaleView(LoginRequiredMixin,TemplateView):
    template_name = 'image_upscale.html'
