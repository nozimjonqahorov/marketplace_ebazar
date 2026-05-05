from django import forms
from .models import Order

class CreateOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["quantity", "phone_number", "message"]
        
        widgets = {
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control rounded-pill',
                'min': '1',
                'placeholder': 'Miqdorni kiriting...'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control rounded-pill',
                'placeholder': '+998 90 123 45 67'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control rounded-4',
                'rows': 3,
                'placeholder': 'Sotuvchiga qo\'shimcha izohingiz bo\'lsa yozing...'
            }),
        }
        
        error_messages = {
            'quantity': {
                'required': 'Mahsulot miqdori kiritilishi shart!',
                'invalid': 'Miqdor son bo\'lishi kerak!',
            },
            'phone_number': {
                'required': 'Telefon raqami kiritilishi shart!',
                'invalid': 'Telefon raqami noto\'g\'ri formatda!',
            },
        }

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity is None:
            raise forms.ValidationError("Mahsulot miqdori kiritilishi shart!")
        if quantity <= 0:
            raise forms.ValidationError("Miqdor 1 tadan kam bo'lishi mumkin emas.")
        if not isinstance(quantity, int):
            raise forms.ValidationError("Miqdor butun son bo'lishi kerak!")
        return quantity
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number and not phone_number.replace('+', '').replace(' ', '').replace('-', '').isdigit():
            raise forms.ValidationError("Telefon raqami noto'g'ri formatda! Faqat raqamlar va +, -, bo'sh joy ishlatilishi mumkin.")
        return phone_number