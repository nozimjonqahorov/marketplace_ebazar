from django.urls import path
from .views import *
urlpatterns = [
    path("hisoblar/", CardListView.as_view(), name="cards-list"),
    path("hisob-yaratish/", CardCreateView.as_view(), name="card-create"),
    path("hisob-detal/<int:pk>/", CardDetailView.as_view(), name="card-detail"),
    path("hisob-tahrir/<int:pk>/", CardUpdateView.as_view(), name="card-update"),
    path("hisob-uchirish/<int:pk>", CardDeleteView.as_view(), name="card-delete"),
]