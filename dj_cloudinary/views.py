import cloudinary.uploader
from django.views.generic import TemplateView,UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
import cloudinary
import cloudinary.uploader
import uuid
from .models import Image
from django.conf import settings
from django.contrib.auth import get_user_model


User = get_user_model()


class ImageUpscaleView(LoginRequiredMixin, TemplateView):
    login_url = "/users/login/"
    redirect_field_name = "next"
    template_name = "cloudinary/image_upscale.html"


def update_image_view(request,public_id):
    image = Image.objects.get(public_id=public_id)
    return render(request,"cloudinary/image_update.html",context={"image":image})




def htmx_upload_image_view(request):
    if request.method != "POST":
        return render(request, "extra/upload_image.html", 
                      context={"error": "Method not allowed"})
    
   
    
    if request.user.upscale_credit == 0:
        return render(request, "extra/upload_image.html", 
                      context={"error": "User have no credit to Upload Image. Please Buy credits first"})
    

    if "image" not in request.FILES:
        return render(request, "extra/upload_image.html", 
                      context={"error": "No image provided"})
    

      
    image_file = request.FILES["image"]

    user_images = request.user.images.all()
    for imgs in user_images:
        if image_file.name == imgs.image_name:
            response = render(request, "extra/upload_image.html", context={
                "image": imgs,
                "message": "Image already exists in your gallery",
                "redirect_url": reverse("scale:update", kwargs={"public_id": imgs.public_id})
            })
            
            return response

    try:
        # Configure Cloudinary once
        cloudinary_init = cloudinary.config(
            cloud_name=settings.CLOUDINARY_CLOUD_NAME,
            api_key=settings.CLOUDINARY_API_KEY,
            api_secret=settings.CLOUDINARY_API_SECRET,
            secure=True,
        )
        if not cloudinary_init:
            return render(request, "extra/upload_image.html", 
                          context={"error": "Cloudinary configuration failed"})
            
        # Generate unique ID and upload
        public_id = str(uuid.uuid4())
        result = cloudinary.uploader.upload(image_file, public_id=public_id)
        
        if "secure_url" not in result:
            return render(request, "extra/upload_image.html", 
                          context={"error": "Upload failed"})
            
        # Create image record and return in one step
        image = Image.objects.create(
            user=request.user,
            public_id=public_id,
            image_name=image_file.name,
            upload_link=result["secure_url"],
        )
        user=User.objects.filter(username=request.user.username).first()
        user.upscale_credit = user.upscale_credit - 1
        user.save()
        return render(request, "extra/upload_image.html", context={"image": image})

    except Exception as e:
        return render(request, "extra/upload_image.html", 
                      context={"error": f"Upload failed: {str(e)}"})





def ai_task_view(request,public_id,task):
    if request.method != "POST":
        return render(request, "extra/result.html", 
                      context={"error": "Method not allowed"})
