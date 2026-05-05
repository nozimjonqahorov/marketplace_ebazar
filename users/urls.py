from django.urls import path
from .views import BuyerSignupView, SellerSignupView, LoginView, logout_view, ProfileView, ProfileUpdateView, ChangePasswordView

urlpatterns = [
    path("buyer-signup/", BuyerSignupView.as_view(), name="buyer_signup"),
    path("seller-signup/", SellerSignupView.as_view(), name="seller_signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", logout_view, name="logout"),
    path("profile/<str:username>/", ProfileView.as_view(), name="profile"),
    path("profile-update/", ProfileUpdateView.as_view(), name="profile-update"),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
]