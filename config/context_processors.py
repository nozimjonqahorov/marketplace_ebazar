"""
Context processor to make categories available in all templates
"""
from products.models import Category

def categories_context(request):
    """Add categories to all template contexts"""
    return {
        'categories': Category.objects.all()
    }
