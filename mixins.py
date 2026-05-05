
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied

class SellerRequiredMixin(UserPassesTestMixin):
    """Faqat sotuvchi rolidagilar kira olishini ta'minlovchi mixin"""
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == 'seller'

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            raise PermissionDenied 
        return super().handle_no_permission()