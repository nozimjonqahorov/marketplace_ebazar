from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignupForm, LoginForm, ProfileUpdateForm
from django.views import View
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .models import CustomUser

class SignupView(View):
    def get(self, request):
        form = SignupForm()
        return render(request, "signup.html", {"form":form})
    
    def post(self, request):
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            raw_password = form.cleaned_data.get("password")
            user.set_password(raw_password)
            user.save()
            return redirect("login")
        
        return render(request, "signup.html", {"form":form})
    

class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("home")
        form = LoginForm()
        return render(request, "login.html", {"form": form})
    
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f"Xush kelibsiz, {user.username}!")
                return redirect("home")
            else:
                messages.error(request, "Username yoki parol xato!") 
        
        return render(request, "login.html", {"form": form})
    

def logout_view(request):
    logout(request)
    return redirect('login')

class ProfileView(View):
    def get(self, request, username):
        user = get_object_or_404(CustomUser.objects.prefetch_related("user_products"), username = username)
        user_products = user.user_products.all()
        return render(request, "profile.html", {"view_user":user, "user_products":user_products})
        

class ProfileUpdateView(LoginRequiredMixin, View):
    def get(self, request):
        form = ProfileUpdateForm(instance=request.user)
        return render(request, "profile_update.html", {"form":form})
    
    def post(self, request):
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("profile")
        return render(request, "profile_update.html", {"form":form})
    

class ChangePasswordView(LoginRequiredMixin, View):
    def get(self, request):
        form = PasswordChangeForm(user=request.user)
        return render(request, "change_password.html", {"form": form})

    def post(self, request):
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect("profile")
        return render(request, "change_password.html", {"form": form})
    
    