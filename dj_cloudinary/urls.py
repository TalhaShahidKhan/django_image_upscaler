from django.urls import path

from .views import ImageUpscaleView,update_image_view,htmx_upload_image_view,ai_task_view


urlpatterns = [
    path('',ImageUpscaleView.as_view(),name="upscale"),
    path('upload/',htmx_upload_image_view,name="upload"),
    path('image/<str:public_id>/',update_image_view,name="update"),
    path('task/<str:public_id>/<str:task>/',ai_task_view,name="task"),
]
app_name = "cloudinary"