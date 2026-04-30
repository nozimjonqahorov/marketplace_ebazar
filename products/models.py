from django.db import models
from users.models import CustomUser
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name
    

class Product(models.Model):

    STATUS = [
        ("sotuvda", "SOTUDA"),
        ("sotilgan", "SOTILGAN")
    ]
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="sotgan_mahsulotlar")
    buyer = models.ForeignKey(CustomUser,null=True, blank=True, on_delete=models.SET_NULL, related_name="sotibolgan_mahsulotlar")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category_products")
    title = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=18, decimal_places=2)
    address = models.CharField(max_length=160)
    status = models.CharField(max_length=20, choices=STATUS)
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
    
class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="author_comments")
    content =models.CharField(340)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f" Commment author: {self.author.username}"



class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Kutilmoqda'),
        ('completed', 'Muvaffaqiyatli'),
        ('canceled', 'Bekor qilindi'),
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="sotuv_zakazlar")
    buyer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="qabul_zakazlar")
    total_price = models.DecimalField(max_digits=18, decimal_places=2)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
