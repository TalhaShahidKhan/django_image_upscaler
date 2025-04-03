from typing import Iterable
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.
class Credit(models.Model):
    product_id = models.CharField(max_length=400,blank=False,null=False)
    number_of_credits = models.PositiveIntegerField(blank=False,null=False)
    price = models.PositiveIntegerField(blank=False,null=False)


    def __str__(self) -> str:
        return f"Credits{self.number_of_credits} > ${self.price}"
    


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    credit = models.ForeignKey(Credit, on_delete=models.SET_NULL, null=True)
    amount = models.PositiveIntegerField(blank=False, null=False)
    checkout_id = models.CharField(max_length=100, blank=True, null=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.amount = self.credit.price if self.credit else 0
        return super().save(force_insert, force_update, using, update_fields)
    
    def __str__(self):
        return f"{self.user} > $ {self.amount}"