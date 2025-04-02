import cloudinary.uploader
from django.views.generic import TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
import cloudinary
from cloudinary import CloudinaryImage
import cloudinary.uploader
import uuid
from .models import Image
from django.conf import settings
from django.contrib.auth import get_user_model


User = get_user_model()


def get_cloudinary_config():
    # Configure Cloudinary once
    cloudinary_init = cloudinary.config(
        cloud_name=settings.CLOUDINARY_CLOUD_NAME,
        api_key=settings.CLOUDINARY_API_KEY,
        api_secret=settings.CLOUDINARY_API_SECRET,
        secure=True,
    )
    return cloudinary_init


class ImageUpscaleView(LoginRequiredMixin, TemplateView):
    login_url = "/users/login/"
    redirect_field_name = "next"
    template_name = "cloudinary/image_upscale.html"


def update_image_view(request, public_id):
    image = Image.objects.get(public_id=public_id)
    return render(request, "cloudinary/image_update.html", context={"image": image})


def htmx_upload_image_view(request):
    if request.method != "POST":
        return render(
            request, "extra/upload_image.html", context={"error": "Method not allowed"}
        )

    if request.user.upscale_credit == 0:
        return render(
            request,
            "extra/upload_image.html",
            context={
                "error": "User have no credit to Upload Image. Please Buy credits first"
            },
        )

    if "image" not in request.FILES:
        return render(
            request, "extra/upload_image.html", context={"error": "No image provided"}
        )

    image_file = request.FILES["image"]

    user_images = request.user.images.all()
    for imgs in user_images:
        if image_file.name == imgs.image_name:
            response = render(
                request,
                "extra/upload_image.html",
                context={
                    "image": imgs,
                    "message": "Image already exists in your gallery",
                    "redirect_url": reverse(
                        "scale:update", kwargs={"public_id": imgs.public_id}
                    ),
                },
            )

            return response

    try:
        cloudinary_init = get_cloudinary_config()
        if not cloudinary_init:
            return render(
                request,
                "extra/upload_image.html",
                context={"error": "Cloudinary configuration failed"},
            )

        # Generate unique ID and upload
        public_id = str(uuid.uuid4())
        result = cloudinary.uploader.upload(image_file, public_id=public_id)

        if "secure_url" not in result:
            return render(
                request, "extra/upload_image.html", context={"error": "Upload failed"}
            )

        # Create image record and return in one step
        image = Image.objects.create(
            user=request.user,
            public_id=public_id,
            image_name=image_file.name,
            upload_link=result["secure_url"],
        )
        user = User.objects.filter(username=request.user.username).first()
        user.upscale_credit = user.upscale_credit - 1
        user.save()
        return render(request, "extra/upload_image.html", context={"image": image})

    except Exception as e:
        return render(
            request,
            "extra/upload_image.html",
            context={"error": f"Upload failed: {str(e)}"},
        )


def ai_task_view(request, public_id, task):
    if request.method != "POST":
        return render(
            request, "extra/result_image.html", context={"error": "Method not allowed"}
        )
    try:
        cloudinary_init = get_cloudinary_config()
        if not cloudinary_init:
            return render(
                request,
                "extra/result_image.html",
                context={"error": "Cloudinary configuration failed"}
            )
            
        # Get the original image to pass to template
        original_image = Image.objects.get(public_id=public_id)
        
        # Process based on task
        if task == "upscale":
            result = CloudinaryImage(public_id).image(effect="upscale")
            return render(
                request,
                "extra/result_image.html",
                context={
                    "url": f"{result[10:-3]}", 
                    "task_name": "Upscaled Image",
                    "original_image": original_image
                }
            )
        elif task == "ext":
            ext = request.POST.get("ext","")
            result = CloudinaryImage(public_id).image(effect=f"extract:prompt_({ext})")
            return render(
                request,
                "extra/result_image.html",
                context={
                    "url": f"{result[10:-3]}", 
                    "task_name": "Extracted Image",
                    "original_image": original_image
                }
            )
        elif task == "bg_remove":
            result = CloudinaryImage(public_id).image(effect="background_removal")
            return render(
                request,
                "extra/result_image.html",
                context={
                    "url": f"{result[10:-3]}", 
                    "task_name": "Background Removed",
                    "original_image": original_image
                }
            )
        elif task == "gen_fill":
            result = CloudinaryImage(public_id).image(
                aspect_ratio="1:1", gravity="center", background="gen_fill", crop="pad"
            )
            return render(
                request,
                "extra/result_image.html",
                context={
                    "url": f"{result[10:-3]}", 
                    "task_name": "Generative Fill",
                    "original_image": original_image
                }
            )
        elif task == "gen_replace":
            try:
                replace_from = request.POST.get("from", "")
                replace_to = request.POST.get("to", "")
                
                if not replace_from or not replace_to:
                    return render(
                        request,
                        "extra/result_image.html",
                        context={"error": "Missing 'from' or 'to' parameters for generative replace"}
                    )
                    
                result = CloudinaryImage(public_id).image(
                    effect=f"gen_replace:from_{replace_from};to_{replace_to}"
                )
                return render(
                    request,
                    "extra/result_image.html",
                    context={
                        "url": f"{result[10:-3]}", 
                        "task_name": f"Replaced '{replace_from}' with '{replace_to}'",
                        "original_image": original_image
                    }
                )
            except KeyError:
                return render(
                    request,
                    "extra/result_image.html",
                    context={"error": "Missing required parameters for generative replace"}
                )
        else:
            return render(
                request,
                "extra/result_image.html",
                context={"error": f"Unknown task: {task}"}
            )
            
    except Image.DoesNotExist:
        return render(
            request,
            "extra/result_image.html",
            context={"error": "Image not found"}
        )
    except Exception as e:
        return render(
            request,
            "extra/result_image.html",
            context={"error": f"Image processing failed: {str(e)}"}
        )
