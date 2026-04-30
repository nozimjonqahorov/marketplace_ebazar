from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Saved


admin.site.site_header = "Mening Admin Panelim"
admin.site.site_title = "Admin Portal"
admin.site.index_title = "Boshqaruv paneliga xush kelibsiz"


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'phone', 'tg_username', 'is_active')
    list_filter = ('is_active', 'is_staff')
    search_fields = ('username', 'first_name', 'last_name', 'phone', 'tg_username')
    
    fieldsets = UserAdmin.fieldsets + (
        ("Qoshimcha", {'fields': ('phone', 'tg_username', 'avatar')}),
    )


@admin.register(Saved)
class SavedAdmin(admin.ModelAdmin):
    list_display = ('author', 'product', 'short_content', 'date')
    list_filter = ('date', 'product')
    search_fields = ('author__username', 'product__title', 'content')
    readonly_fields = ('date',)
    
    def short_content(self, obj):
        return obj.content[:50] if len(obj.content) > 50 else obj.content
    short_content.short_description = 'Kontent'

