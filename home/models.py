from django.db import models

# Create your models here.


class ContactFormFeedback(models.Model):
    email=models.EmailField(blank=False,null=False)
    feedback=models.TextField(blank=False,null=False)
    def __str__(self) -> str:
        return f"{self.email}"