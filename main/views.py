from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from products.models import Product, Category, ProductView
from users.models import Saved
from django.db.models import Count
from django.core.paginator import Paginator


class HomepageView(View):
    def get(self, request):
        categories = Category.objects.all()

        if request.user.is_authenticated and request.user.role == 'seller':
            products_qs = Product.objects.filter(author=request.user).select_related(
                "category", "author"
            ).order_by("-date")
            total_products_count = products_qs.count()

            paginator = Paginator(products_qs, 12)
            page_num = request.GET.get("page", 1)
            products_page = paginator.get_page(page_num)

            total_seller_views = ProductView.objects.filter(
                product__author=request.user
            ).count()

            context = {
                "products": products_page,
                "categories": categories,
                "total_seller_views": total_seller_views,
                "total_products_count": total_products_count,
            }
        else:
            
            products = Product.objects.filter(is_active=True, quantity__gt=0).select_related(
                "category", "author"
            ).order_by("-date")[:8]

            most_viewed = (
                Product.objects.filter(is_active=True, quantity__gt=0)
                .annotate(total_views=Count("product_views"))
                .select_related("category", "author")
                .order_by("-total_views")[:8]
            )

            saved_ids = []
            if request.user.is_authenticated:
                saved_ids = Saved.objects.filter(author=request.user).values_list(
                    "product_id", flat=True
                )

            context = {
                "products": products,
                "categories": categories,
                "saved_ids": saved_ids,
                "most_viewed": most_viewed,
            }

        return render(request, "home.html", context)
