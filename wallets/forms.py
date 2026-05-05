from django import forms
from .models import Card

class CardCreateForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ['name', 'balance', 'card_number', "is_primary"]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Bank nomi'
            }),
            'balance': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00'
            }),
            'card_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '1234 5678 9012 3456',
                'maxlength': '16'
            }),
        }