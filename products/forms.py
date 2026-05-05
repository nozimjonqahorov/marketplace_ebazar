from django import forms 
from .models import Product, ProductImage, Comment
from django.forms import inlineformset_factory



class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["title", "category", "description", "price", "quantity", "condition", "address"]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'condition': forms.Select(attrs={'class': 'form-select'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
        }


ImageFormSet = inlineformset_factory(
    Product,            # Ota model
    ProductImage,       # Bog'langan model
    fields=('image',),  # Faqat rasm maydoni
    extra=3,            # Bir vaqtda nechta rasm yuklash joyi chiqsin?
    can_delete=True
)


class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["title", "category", "description","quantity", "price", "address", "is_active"]


ImageUpdateFormSet = inlineformset_factory(
    Product,            # Ota model
    ProductImage,       # Bog'langan model
    fields=('image',),  # Faqat rasm maydoni
    extra=0,            # Bir vaqtda nechta rasm yuklash joyi chiqsin?
    can_delete=True

)



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Fikringizni yozing...',
                'rows': 3
            }),
        }