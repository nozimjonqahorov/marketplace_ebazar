from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from products.models import Product, Category
# Create your views here.



class HomepageView(View):
    def get(self, request):
        products = Product.objects.all().select_related('category', 'author')[:6]

        categories = Category.objects.all()
        
        context = {
            "products": products,
            "categories": categories
        }
        return render(request, "home.html", context)
    

    
def categories_for_pages(request):
    categories =  Category.objects.all()
    return {"categories":categories}


class CategoryView(View):
    def get(self, request, category_name):
        category = get_object_or_404(
            Category.objects.prefetch_related('category_products'), 
            name=category_name
        )
        return render(request, "category.html", {
            "category": category,
            "category_products": category.category_products.all()
        })