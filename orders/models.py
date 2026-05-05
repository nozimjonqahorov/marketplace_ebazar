from django.db import models
from users.models import CustomUser
from products.models import Product

class Order(models.Model):
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="orders")
    buyer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="my_orders")
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="received_orders")
    quantity = models.PositiveIntegerField(default=1)
    phone_number = models.CharField(max_length=17, blank=True, null=True) 
    total_price = models.DecimalField(max_digits=18, decimal_places=2, editable=False, null=True, blank=True)
    message = models.TextField(blank=True) 
    
    status = models.CharField(max_length=20, choices=[
        ('new', 'Yangi'),
        ('accepted', 'Qabul qilindi'),
        ('completed', 'Yakunlandi'),
        ('canceled', 'Bekor qilindi')
    ], default='new')
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.product.title}"