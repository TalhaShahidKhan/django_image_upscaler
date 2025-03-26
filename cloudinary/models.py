from django.db import models
from django.contrib.auth import  get_user_model

User = get_user_model()
# Create your models here.
class UploadImageModel(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,blank=False,null=False,related_name="images")
    upload_link=models.CharField(max_length=1000,blank=False,null=True)