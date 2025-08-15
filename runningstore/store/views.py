from django.shortcuts import render, redirect
from .models import Product # Import the Product model
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from.forms import SignUpForm, UpdateUserForm, ChangePasswordForm
from django.core.exceptions import ObjectDoesNotExist
from .models import Category


def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        #did they fill out the form
        if request.method =='POST':
            pass 
        else:
            form = ChangePasswordForm(current_user)
            return render(request, "update_password.html", {'form': form })
    else:
        messages.success(request,"You Need To Be Logged in Tp View That!!")
        return redirect('home')








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
    
    else:
        
        return render(request, 'register.html', {'form': form})


def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product': product})

def category(request, foo):
    # Replace hyphens with spaces in the category name from the URL
    category_name = foo.replace('-', ' ')
    
    try:
        category = Category.objects.get(name__iexact=category_name)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {
            'products': products,
            'category': category
        })
    
    except ObjectDoesNotExist:
        messages.error(request, "That category doesn't exist")
        return redirect('home')
    
def category_summary(request):
    categories = Category.objects.all()
    return render(request, 'category_summary.html', {'categories': categories}) 
    
def update_user(request):

    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)

        if user_form.is_valid():
            user_form.save()
            messages.success(request, "Your profile has been updated successfully.")
            login(request, current_user)
            return redirect('home')

        
        return render(request, 'update_user.html', {'user_form': user_form})
    else:
        messages.error(request, "You need to be logged in to update your profile.")
        return redirect('login')

def update_password(request):
    return render(request, "update_password.html", {})