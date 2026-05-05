from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CardCreateForm
from .models import Card


class CardListView(LoginRequiredMixin, View):
    def get(self, request):
        cards = Card.objects.filter(user = request.user)
        return render(request, "cards_list.html", {"cards":cards})
    

class CardCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = CardCreateForm()
        return render(request, "card_create.html", {"form": form})
    
    def post(self, request):
        form = CardCreateForm(request.POST)
        if form.is_valid():
            card = form.save(commit = False)
            card.user = request.user
            card.save()
            return redirect("cards-list")
        return render(request, "card_create.html", {"form":form})
    

class CardDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        card = get_object_or_404(Card, pk=pk)
        return render(request, "card_detail.html", {"card": card})
    
class CardUpdateView(LoginRequiredMixin, View):
    def get(self, request, pk): 
        card = get_object_or_404(Card, pk = pk, user = request.user)
        form  = CardCreateForm(instance = card)
        return render(request, "card_update.html", {"form":form, "card":card})
    
    def post(self, request, pk):
        card = get_object_or_404(Card, pk = pk, user = request.user)
        form = CardCreateForm(request.POST, instance = card)
        if form.is_valid():
            card = form.save(commit = False)
            card.user = request.user
            card.save()
            return redirect("card-detail", pk)
        return render(request, "card_update.html", {"form":form, "card":card})
    

class CardDeleteView(LoginRequiredMixin, View):
    def get(self, request, pk):
        card = get_object_or_404(Card, pk = pk, user = request.user)
        return render(request, "card_delete.html", {"Card":card})
    
    def post(self, request, pk):
        card = get_object_or_404(Card, pk = pk, user = request.user)
        card.delete()
        return redirect("cards-list")


            
                




        