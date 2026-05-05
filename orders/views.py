from django.shortcuts import render, redirect, get_object_or_404
from .models import Order
from users.models import CustomUser
from wallets.models import Card
from products.models import Product
from django.http import HttpResponseForbidden
from django.views import View
from mixins import SellerRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CreateOrderForm
from django.db.models import Sum
from django.contrib import messages
from django.db import transaction

class SellerDashboardView(SellerRequiredMixin, View):
    def get(self, request):
        if request.user.role != "seller":
            return HttpResponseForbidden
        
        my_products = Product.objects.filter(author = request.user).order_by("-date")
        my_orders = Order.objects.filter(seller = request.user).order_by("-created_at")
        total_products = my_products.count()
        total_orders = my_orders.count()

        
        completed_orders = my_orders.filter(status='completed')
        total_income = completed_orders.aggregate(total=Sum('total_price'))['total'] or 0
        
        total_views = sum(p.product_views.count() for p in my_products)

        context = {
            'products': my_products,
            "my_orders": my_orders,
            'total_products': total_products,
            'total_orders': total_orders,
            'total_views': total_views,
            'total_income': int(total_income),
        }
        return render(request, 'orders/seller_dashboard.html', context)


class CreateOrderView(LoginRequiredMixin, View):
    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        form = CreateOrderForm()
        user_cards = Card.objects.filter(user=request.user)
        
        context = {
            "form": form,
            "product": product,
            "user_cards": user_cards
        }
        return render(request, "orders/create_order.html", context)
    
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        card_id = request.POST.get('card_id')
        
  
        quantity_str = request.POST.get("quantity", "1")
        try:
            quantity = int(quantity_str)
        except (ValueError, TypeError):
            messages.error(request, "Miqdor noto'g'ri! Faqat butun sonlar ishlatilsin.")
            return redirect('create_order', product_id=product.id)
        
       
        if quantity <= 0:
            messages.error(request, "Miqdor 1 tadan kam bo'lishi mumkin emas!")
            return redirect('create_order', product_id=product.id)
        
       
        if quantity > product.quantity:
            messages.error(request, f"Zaxirada yetarli mahsulot yo'q! Mavjud: {product.quantity} ta")
            return redirect('create_order', product_id=product.id)
        
        total_price = product.price * quantity

        
        if not card_id:
            messages.error(request, "Iltimos, to'lov kartasini tanlang!")
            return redirect('create_order', product_id=product.id)

        try:
            with transaction.atomic():
                buyer_card = get_object_or_404(Card, id=card_id, user=request.user)

                if buyer_card.balance < total_price:
                    messages.error(request, f"Kartangizda mablag' yetarli emas! Kerak: {total_price} so'm, Mavjud: {buyer_card.balance} so'm")
                    return redirect('create_order', product_id=product.id)

                buyer_card.balance -= total_price
                buyer_card.save()

                order = Order.objects.create(
                    product=product,
                    buyer=request.user,
                    seller=product.author,
                    quantity=quantity,
                    total_price=total_price,
                    status='new'
                )

                
                product.quantity -= quantity
                if product.quantity == 0:
                    product.is_active = False
                product.save()

                messages.success(request, f" To'lov amalga oshirildi! {total_price} so'm yozildi. Sotuvchi mahsulotni yetkazishini kuting.")
                return redirect('my_orders') 

        except Exception as e:
            messages.error(request, f"Xatolik yuz berdi: {str(e)}")
            return redirect('create_order', product_id=product.id)


class CompleteOrderView(LoginRequiredMixin, View):
    def post(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, seller=request.user)

        if order.status != 'accepted':
            messages.error(request, " Bu buyurtmani yakunlab bo'lmaydi! Faqat 'Yetkazilmoqda' holatidagi buyurtmalarni yakunlash mumkin.")
            return redirect('seller_dashboard')

        try:
            with transaction.atomic():
                seller_card = Card.objects.filter(user=request.user, is_primary=True).first() or \
                              Card.objects.filter(user=request.user).first()

                if not seller_card:
                    messages.error(request, " Hisobingizga pul tushishi uchun karta ulashing!")
                    return redirect('seller_dashboard')

                seller_card.balance += order.total_price
                seller_card.save()

                order.status = 'completed'
                order.save()

                messages.success(request, f" Buyurtma yakunlandi! {order.total_price} so'm hisobingizga o'tdi.")
        except Exception as e:
            messages.error(request, f"Xatolik: {str(e)}")

        return redirect('seller_dashboard')


class AcceptOrderView(LoginRequiredMixin, View):
    def post(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, seller=request.user)

        if order.status != 'new':
            messages.error(request, "Faqat yangi buyurtmalarni qabul qilish mumkin!")
            return redirect('seller_dashboard')

        order.status = 'accepted'
        order.save()
        messages.success(request, f" Buyurtma qabul qilindi! Xaridor {order.product.title} yetkazilishini kutmoqda.")
        return redirect('seller_dashboard')


class CancelOrderView(LoginRequiredMixin, View):
    def post(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)

        if request.user != order.buyer and request.user != order.seller:
            messages.error(request, "Ruxsat berilmagan! Siz bu buyurtmani o'zgartira olmaysiz.")
            return redirect('home')

        if order.status == 'completed':
            messages.error(request, " Bu buyurtma yakunlangan, bekor qilib bo'lmaydi.")
            return redirect('seller_dashboard' if request.user == order.seller else 'my_orders')

        if order.status in ('new', 'accepted'):
            try:
                with transaction.atomic():
                    buyer_card = Card.objects.filter(user=order.buyer, is_primary=True).first() or \
                                 Card.objects.filter(user=order.buyer).first()

                    if not buyer_card:
                        messages.error(request, " Xaridorga qaytarish uchun karta topilmadi!")
                        return redirect('seller_dashboard' if request.user == order.seller else 'my_orders')

                    buyer_card.balance += order.total_price
                    buyer_card.save()

                    order.product.quantity += order.quantity
                    order.product.is_active = True
                    order.product.save()

                    order.status = 'canceled'
                    order.save()

                    if request.user == order.buyer:
                        messages.warning(request, f" Buyurtma bekor qilindi! ")
                    else:
                        messages.warning(request, f" Buyurtma bekor qilindi! ")
            except Exception as e:
                messages.error(request, f"Xatolik: {str(e)}")

        return redirect('seller_dashboard' if request.user == order.seller else 'my_orders')
  

class MyOrdersView(LoginRequiredMixin, View):
    def get(self, request):
        orders = Order.objects.filter(buyer=request.user).order_by("-created_at")

        total_orders = orders.count()
        total_products = orders.values("product_id").distinct().count()
        
       
        total_expense = orders.filter(status='completed').aggregate(total=Sum('total_price'))['total'] or 0

        context = {
            "orders": orders,
            "total_orders": total_orders,
            "total_products": total_products,
            "total_expense": int(total_expense),
        }
        return render(request, "orders/my_orders.html", context)


class OrderDetailView(LoginRequiredMixin, View):
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        
        if request.user != order.buyer and request.user != order.seller:
            messages.error(request, " Siz bu buyurtmani ko'ra olmaysiz!")
            return redirect('home')
        
        context = {
            'order': order,
        }
        return render(request, 'orders/order_detail.html', context)
