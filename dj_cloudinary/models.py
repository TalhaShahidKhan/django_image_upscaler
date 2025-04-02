from django.db import models
from django.contrib.auth import  get_user_model

User = get_user_model()
# Create your models here.
class Image(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=False,null=False,related_name="images")
    public_id = models.CharField(max_length=220,blank=False,null=True)
    image_name = models.CharField(max_length=110,blank=True,null=True)
    upload_link=models.CharField(max_length=1000,blank=False,null=True)

    def __str__(self) -> str:
        return f"{self.user} > {self.image_name}"