from django.urls import path
from .views import *
urlpatterns = [
    path("seller-dashboard/", SellerDashboardView.as_view(), name="seller_dashboard"),
    path('product/<int:product_id>/order/', CreateOrderView.as_view(), name='create_order'),
    path('order/<int:order_id>/', OrderDetailView.as_view(), name='order_detail'),
    path('accept-order/<int:order_id>/accept/', AcceptOrderView.as_view(), name='accept_order'),
    path('complete-order/<int:order_id>/complete/', CompleteOrderView.as_view(), name='complete_order'),
    path('cancel-order/<int:order_id>/cancel/', CancelOrderView.as_view(), name='cancel_order'),
    path('my-orders/', MyOrdersView.as_view(), name='my_orders'),
]
