from django.db import models
from users.models import CustomUser
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name
    

class Product(models.Model):

    CHOICES = [
        ("new", "Yangi"),
        ("used", "Ishlatilgan"),
        ("old", "Eski"),
    ]
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="user_products")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category_products")
    title = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=18, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1) 
    address = models.CharField(max_length=160)
    condition = models.CharField(max_length=20, choices=CHOICES, default="new")
    is_active = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title 


class ProductImage(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    image = models.ImageField(upload_to="products", default="products/defautl_product.png")

    def __str__(self):
        return f"Photo of {self.product.title}"
    
class ProductView(models.Model):
    product = models.ForeignKey(
        "products.Product", 
        on_delete=models.CASCADE, 
        related_name="product_views"
    )
    user = models.ForeignKey(
        CustomUser, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name="user_view_history"
    )
    session_key = models.CharField(max_length=40, null=True, blank=True) # Anonim foydalanuvchilar uchun
    viewed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        username = self.user.username if self.user else "Anonim"
        return f"{self.product.title} ko'rildi: {username} - {self.viewed_at}"
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'product'], 
                name='unique_user_product_view',
                condition=models.Q(user__isnull=False) 
            ),
            models.UniqueConstraint(
                fields=['session_key', 'product'], 
                name='unique_session_product_view',
                condition=models.Q(session_key__isnull=False)
            )
        ]
    
class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.CharField(max_length=500)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f" Commment author: {self.author.username}"



