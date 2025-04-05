from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.
class Credit(models.Model):
    number_of_credits = models.PositiveIntegerField(blank=False,null=False)
    price = models.PositiveIntegerField(blank=False,null=False)


    def __str__(self) -> str:
        return f"Credits{self.number_of_credits} > ${self.price}"
    


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    credit = models.ForeignKey(Credit, on_delete=models.SET_NULL, null=True)
    amount = models.PositiveIntegerField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user} > $ {self.amount}"