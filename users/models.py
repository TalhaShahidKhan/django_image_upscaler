from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import CustomUserManager
# Create your models here.



class CustomUser(AbstractUser):
    upscale_credit = models.PositiveIntegerField(default=3)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    objects = CustomUserManager()


    def __str__(self):
        return self.username