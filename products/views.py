from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProductForm, ImageFormSet, ProductUpdateForm, ImageUpdateFormSet, CommentForm
from django.views import View
from .models import Product, Category, ProductImage, Comment, ProductView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseForbidden
from django.forms import inlineformset_factory
from django.db.models import Q
from users.models import Saved
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.urls import reverse
from mixins import SellerRequiredMixin
from wallets.models import Card
from django.contrib import messages

class CreateProductView(SellerRequiredMixin, View):
    def get(self, request):
        has_card = Card.objects.filter(user=request.user).exists()
        if not has_card:
            messages.error(request, "Sotish uchun avval hisob (card) qo‘shishingiz kerak.")
            return redirect("card-create")

        form = ProductForm()
        formset = ImageFormSet()
        categories = Category.objects.all()
        return render(request, "create_product.html", {"form": form, "formset": formset, "categories": categories})

    def post(self, request):
        has_card = Card.objects.filter(user=request.user).exists()
        if not has_card:
            messages.error(request, "Sotish uchun avval hisob (card) qo‘shishingiz kerak.")
            return redirect("card-create")

        form = ProductForm(request.POST, request.FILES)
        formset = ImageFormSet(request.POST, request.FILES)
        if form.is_valid() and formset.is_valid():
            product = form.save(commit=False)
            product.author = request.user
            product.save()
            formset.instance = product
            formset.save()
            return redirect("home")

        categories = Category.objects.all()
        return render(request, "create_product.html", {"form": form, "formset": formset, "categories": categories})
    

class ProductListView(View):
    def get(self, request):
        categories = Category.objects.all()
        products = Product.objects.filter(is_active=True, quantity__gt=0).select_related('category', 'author').order_by("-date")
        title = "Barcha Mahsulotlar"

        saved_ids = []
        if request.user.is_authenticated:
            saved_ids = Saved.objects.filter(author=request.user).values_list('product_id', flat=True)

        category_id = request.GET.get('category')
        if category_id:
            products = products.filter(category_id=category_id)
            cat_obj = categories.filter(id=category_id).first()
            if cat_obj:
                title = f"{cat_obj.name} kategoriyasidagi mahsulotlar"


        min_price = request.GET.get("min_price")
        max_price = request.GET.get("max_price")

        if min_price and min_price.isdigit():
            products = products.filter(price__gte=min_price)
        
        if max_price and max_price.isdigit():
            products = products.filter(price__lte=max_price)

        query = request.GET.get('q')
        if query:
            products = products.filter(
                Q(title__icontains=query) | 
                Q(description__icontains=query) | 
                Q(address__icontains=query)
            )
        

        paginator = Paginator(products, 12) 
        page_num = request.GET.get('page') 
        page_obj = paginator.get_page(page_num)

        context = {
            "products": page_obj,
            "title": title,
            "saved_ids": saved_ids,
            "categories": categories,
        }
        return render(request, "catalog.html", context)
    

class ProductDetailView(View):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)

        comments = Comment.objects.filter(product=product).order_by('-date')
        form = CommentForm()

        
        same_category_products = Product.objects.filter(
            category=product.category, 
            is_active=True, 
            quantity__gt=0
        ).exclude(pk=pk)[:4]
        categories = Category.objects.all()
        
        if request.user.is_authenticated:
            ProductView.objects.get_or_create(product=product, user=request.user)
        else:
            if not request.session.session_key:
                request.session.create()
            
            session_key = request.session.session_key
            ProductView.objects.get_or_create(product=product, session_key=session_key)    


        context = {
            "product": product,
            "categories": categories,
            "same_category_products": same_category_products,
            "comments": comments, 
            "form": form        
        }
        return render(request, "product_detail.html", context)
    
    def post(self, request, pk):
        product = get_object_or_404(Product, pk = pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = product
            comment.author = request.user
            comment.save()
            return redirect("product_detail", pk)

    

class ProductUpdateView(SellerRequiredMixin, View):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        if product.author != request.user: 
            return HttpResponseForbidden("Siz faqat o'zingiz yaratgan mahsulotni tahrirlay olasiz!")
        
        existing_images_count = product.productimage_set.count()
        new_extra = max(0, 3 - existing_images_count)

        ImageUpdateFormSet = inlineformset_factory(
            Product, ProductImage, fields=('image',), extra=new_extra, can_delete=True
        )
        form = ProductUpdateForm(instance=product)
        formset = ImageUpdateFormSet(instance=product)

        categories = Category.objects.all()
        return render(request, "product_update.html", {"form": form, "formset":formset, "product": product, "categories": categories})

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        if product.author != request.user: 
            return HttpResponseForbidden("Taqiqlangan!")
        

        existing_images_count = product.productimage_set.count()
        new_extra = max(0, 3 - existing_images_count)

        ImageUpdateFormSet = inlineformset_factory(
            Product, ProductImage, fields=('image',), extra=new_extra, can_delete=True
        )

        form = ProductUpdateForm(request.POST, request.FILES, instance=product)
        formset = ImageUpdateFormSet(request.POST, request.FILES, instance=product)

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect("home")
        categories = Category.objects.all()
        return render(request, "product_update.html", {"form": form, "formset":formset, "product": product, "categories": categories})

class ProductDeleteView(SellerRequiredMixin, View):
    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        if product.author != request.user: 
            return HttpResponseForbidden("Boshqa foydalanuvchining narsasini o'chira olmaysiz!")
        
        product.delete()
        return redirect("home")
    


class ToggleSavedView(View):
    def get(self, request, product_id):
        if not request.user.is_authenticated:
            return JsonResponse(
                {"status": "login_required", "login_url": reverse("login")},
                status=401,
            )

        product = get_object_or_404(Product, pk=product_id)
        saved_item = Saved.objects.filter(product=product, author=request.user)

        if saved_item.exists():
            saved_item.delete()
            status = "removed"
        else:
            Saved.objects.create(product=product, author=request.user)
            status = "added"

        return JsonResponse({"status": status})


        
class SavedView(LoginRequiredMixin, View):
    def get(self, request):
        saved_products = Saved.objects.filter(author = request.user).order_by("-date")
        categories = Category.objects.all()
        return render(request, "saved_products.html", {"saved_products":saved_products, "categories":categories})
