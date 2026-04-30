from django.contrib import admin
from .models import Category, Product, ProductImage, Comment

admin.site.site_header = "Mening Admin Panelim"
admin.site.site_title = "Admin Portal"
admin.site.index_title = "Boshqaruv paneliga xush kelibsiz"

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'price', 'date')
    list_filter = ('category', 'date')
    search_fields = ('title', 'description', 'author__username')
    readonly_fields = ('date',)
    inlines = [ProductImageInline]


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'image')
    search_fields = ('product__title',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'product', 'short_content', 'date')
    list_filter = ('date', 'product')
    search_fields = ('author__username', 'product__title', 'content')
    readonly_fields = ('date',)
    
    def short_content(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    short_content.short_description = 'Kontent'