import os
import django
import requests
import random
from django.core.files import File
from io import BytesIO
from decimal import Decimal

# Django sozlamalari
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Product, ProductImage, Category
from users.models import CustomUser

def run():
    # 1. Tozalash (ixtiyoriy, agar hammasini noldan qilmoqchi bo'lsangiz)
    print("Tayyorlanmoqda...")
    
    seller = CustomUser.objects.filter(role="seller").first()
    if not seller:
        # Agar seller bo'lmasa, birinchisini olamiz
        seller = CustomUser.objects.first()

    categories = list(Category.objects.all())
    if not categories:
        print("Kategoriyalar topilmadi!")
        return

    print("20 ta mahsulot yuklanmoqda...")
    
    for i in range(20):
        category = random.choice(categories)
        # Picsum API - har safar har xil rasm olish uchun i (index) ishlatamiz
        img_url = f"https://picsum.photos/seed/{random.randint(1, 1000)}/800/600"
        
        try:
            # Mahsulot yaratish
            product = Product.objects.create(
                author=seller,
                category=category,
                title=f"{category.name} mahsuloti #{i+1}",
                description="Tezkor yuklangan sifatli mahsulot tavsifi.",
                price=Decimal(random.randint(50000, 5000000)),
                quantity=random.randint(1, 10),
                address="Toshkent shahri",
                condition="new",
                is_active=True
            )

            # Rasm yuklash (Eng muhim qismi)
            resp = requests.get(img_url, timeout=10)
            if resp.status_code == 200:
                img_temp = BytesIO(resp.content)
                product_image = ProductImage(product=product)
                product_image.image.save(f"fast_prod_{product.id}.jpg", File(img_temp), save=True)
                print(f"{i+1}/20: {product.title} yuklandi.")
            
        except Exception as e:
            print(f"Xato: {e}")

    print("\nBajarildi! Endi brauzerni tekshiring.")

if __name__ == "__main__":
    run()