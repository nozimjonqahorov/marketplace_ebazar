from django.urls import path
from .views import HomepageView, CategoryView

urlpatterns = [
    path("", HomepageView.as_view(), name = "home"),
    path("<str:category_name>/category>", CategoryView.as_view(), name="category"),
]
