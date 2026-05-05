from django.db import models
from creditcards.models import CardNumberField
from users.models import CustomUser
# Create your models here.
class Card(models.Model):
    """Hisob raqam"""

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="cards")
    name = models.CharField(max_length=30)
    balance = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    card_number = CardNumberField(unique = True, help_text="16 xonali karta raqamini kiriting")
    is_primary = models.BooleanField(default=False) 

    def save(self, *args, **kwargs):
        if self.is_primary:
            Card.objects.filter(user=self.user, is_primary=True).exclude(pk=self.pk).update(is_primary=False)
        super().save(*args, **kwargs)
   
    def __str__(self):
       return f"{self.name} ="
    
    class Meta:
        constraints = [
                models.CheckConstraint(
                    condition=models.Q(balance__gte=0), 
                    name="balance_negative_bolmasin"
                ),
            ]