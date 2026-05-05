from django.urls import path
from .views import ProductDeleteView, CreateProductView, ProductDetailView, ProductListView, ProductUpdateView, ToggleSavedView, SavedView

urlpatterns = [
    path("all-products/", ProductListView.as_view(),name="all_products"),
    path("create-product/", CreateProductView.as_view(),name="create_product"),
    path("update-product/<int:pk>/", ProductUpdateView.as_view(),name="product_update"),
    path("detail-product/<int:pk>/", ProductDetailView.as_view(),name="product_detail"),
    path("delete-product/<int:pk>/", ProductDeleteView.as_view(),name="delete_product"),
    path("save-product/<int:product_id>/", ToggleSavedView.as_view(),name="save_product"),
    path("saved-products/", SavedView.as_view(),name="saved_products"),
]
