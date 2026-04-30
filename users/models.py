from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    phone = models.CharField(max_length=17)
    tg_username = models.CharField(max_length=50)
    avatar = models.ImageField(upload_to="users/", default="users/default_user.png")
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.first_name} | {self.last_name} "
    

class Saved(models.Model):
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="saved")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Author: {self.author.username}, product: {self.product.title}"