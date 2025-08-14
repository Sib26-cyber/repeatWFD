from django.shortcuts import render, redirect
from .models import Product # Import the Product model
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from.forms import SignUpForm

def home(request):
    # Fetch all products from the database
    products = Product.objects.all()
    """
    Render the home page of the running store.
    """
    return render(request, 'home.html', {'products': products})

# Create your views here.
def about(request):
    
    return render(request, 'about.html', {})

def login_user(request): 
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in successfully.")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")   
    
    return render(request, 'login.html', {})


def logout_user(request):

    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect( 'home')

def register_user(request):
    form = SignUpForm
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            # Authenticate the user after registration
            user = authenticate(username=username, password=password)           
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('home')
    else:
        messages.error(request, "Registration failed. Please try again.")
        return redirect('register')

    return render(request, 'register.html', {'form': form})
