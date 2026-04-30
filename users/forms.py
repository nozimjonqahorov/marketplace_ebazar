from django import forms
from users.models import CustomUser 
from django.core.exceptions import ValidationError

class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Parol")
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Parolni tasdiqlash")

    class Meta:
        model = CustomUser
        fields = ["username", "first_name", "last_name", "email", "password"]

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if len(username) < 4:
            raise ValidationError("Username kamida 4-ta elementdan iborat bo'lishi kerak")
        if username.isdigit():
            raise ValidationError("Username faqat sonlardan iborat bo'lishi mumkin emas")
        return username

    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name")
        if len(first_name) < 3:
            raise ValidationError("Ism 3-ta harfdan kam bo'lishi mumkin emas")
        if not first_name.isalpha():
            raise ValidationError("Ism faqat harflardan iborat bo'lishi shart")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get("last_name")
        if len(last_name) < 3:
            raise ValidationError("Familiya 3-ta harfdan kam bo'lishi mumkin emas")
        if not last_name.isalpha():
            raise ValidationError("Familiya faqat harflardan iborat bo'lishi shart")
        return last_name

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise ValidationError("Parollar bir-biriga mos kelmadi!")
        
        return cleaned_data
    

class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length = 30, widget = forms.PasswordInput)


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["username", "first_name", "last_name","tg_username", "phone", "email", "avatar"]

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if username:
            if len(username) < 4:
                raise ValidationError("Username kamida 4-ta elementdan iborat bo'lishi kerak")
            if username.isdigit():
                raise ValidationError("Username faqat sonlardan iborat bo'lishi mumkin emas")
        return username

    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name")
        if first_name:
            if len(first_name) < 3:
                raise ValidationError("Ism 3-ta harfdan kam bo'lishi mumkin emas")
            if not first_name.isalpha():
                raise ValidationError("Ism faqat harflardan iborat bo'lishi shart")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get("last_name")
        if last_name:
            if len(last_name) < 3:
                raise ValidationError("Familiya 3-ta harfdan kam bo'lishi mumkin emas")
            if not last_name.isalpha():
                raise ValidationError("Familiya faqat harflardan iborat bo'lishi shart")
        return last_name

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email and len(email) < 8:
            raise ValidationError("Email kamida 8-ta elementdan iborat bo'lishi kerak")
        return email