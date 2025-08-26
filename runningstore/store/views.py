from django.shortcuts import render,get_object_or_404, redirect
from .models import Product, Category, Profile, Item, Order, Return, Refund
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from.forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
from django import forms
from django.utils import timezone
from django.db.models import Q
import json
from cart.cart import Cart
from payment.models import ShippingAddress
from payment.forms import ShippingForm




        

# Create your views here.              

def home(request):
    # Fetch all products from the database
    products = Product.objects.all()
    """
    Render the home page of the running store.
    """
    return render(request, 'home.html', {'products': products})


def about(request):    
    return render(request, 'about.html', {})

def search(request):
    #check if the form has been submitted
    if request.method == "POST":
        searched = request.POST['searched']
        #Query the products database model to find products that match the search term
        searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched) | Q(category__name__icontains=searched))
        #Test for null
        if not searched:
            messages.info(request, "No products matched your search criteria. Please try again.")
        #look for products that match the search term
        return render(request, 'search.html', {'searched': searched})
    else:
        return render(request, 'search.html', {})
    
    return render(request, 'search.html', {})



def login_user(request): 
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            #Do some shopping cart stuff here
            current_user = Profile.objects.get(user__id = request.user.id)
            #Get the old cart from the Database
            saved_cart = current_user.old_cart
            #Convert the string to a dictionary
            if saved_cart:
                converted_cart = json.loads(saved_cart)
                cart =Cart(request)
                #Loop through the dictionary and add items to the cart
                for key, value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)

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
    except Category.DoesNotExist:
        messages.error(request, "Category not found.")
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

        
        return render(request, 'update_user.html', {'user_form': user_form })
    else:
        messages.error(request, "You need to be logged in to update your profile.")
        return redirect('login')
    


    
def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        #did they fill out the form
        if request.method =='POST':
            form = ChangePasswordForm(current_user, request.POST)
            if form.is_valid():
                user= form.save()                
                messages.success(request, "Your password has been Updated", "Please log in again")              
                return redirect('login')
            
            else:
                for error in list( form.errors.values()):
                    messages.error(request, error)                
                return render(request,"update_password.html", {'form':form})
            
        else: #GET request
            form = ChangePasswordForm(user= current_user)
            return render(request, "update_password.html", {'form': form})
    else:
        messages.success(request, "You must be logged in to view that page")
        return redirect('login')
    
def update_info(request):
    if request.user.is_authenticated:
        #Get the current user's profile
        current_user = Profile.objects.get(user__id = request.user.id)
        #Get Current Users Shipping Info
        shipping_user = ShippingAddress.objects.get(shipping_user__id=request.user.id)
        #Get original user info
        form = UserInfoForm(request.POST or None, instance = current_user)        
        
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        if form.is_valid() or shipping_form.is_valid():
            shipping_form.save()
            form.save()

            messages.success(request, "Your profile has been updated successfully.")            
            return redirect('home')        
        return render(request, 'update_info.html', {'form': form, 'shipping_form': shipping_form})
    else:
        messages.error(request, "You need to be logged in to update your profile.")
        return redirect('home')
    
def item_list(request):
    context = {'items': Item.objects.all()}
        
    return render(request, 'item_list.html',context)

def request_return(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == "POST":
        reason = request.POST.get("reason")
        Return.objects.create(order=order, reason=reason)
        return redirect("order_history")  # redirect to a page showing orders
    return render(request, "request_return.html", {"order": order})

def process_return(request, return_id, action):
    return_request = get_object_or_404(Return, id=return_id)
    if action == "approve":
        return_request.status = "Approved"
    elif action == "reject":
        return_request.status = "Rejected"
    return_request.save()
    return redirect("return_list")

def issue_refund(request, return_id):
    return_request = get_object_or_404(Return, id=return_id, status="Approved")
    order = return_request.order

    Refund.objects.create(
        order=order,
        return_request=return_request,
        reason=return_request.reason,
        amount=order.total_amount,  # refund full amount for simplicity
        refund_date=timezone.now(),
        processed=True
    )
    return_request.status = "Completed"
    return_request.save()

    return redirect("refund_list")

