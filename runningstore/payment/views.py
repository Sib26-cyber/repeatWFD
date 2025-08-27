from django.shortcuts import render, redirect
from cart.cart import Cart
from django.contrib import messages
from payment.models import ShippingAddress
from payment.forms import ShippingForm

# Create your views here.
def payment_success(request):
    return render(request, 'payment/payment_success.html', {})



def billing_info(request):    
    if request.POST:

         
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()
        shipping_form = request.POST             

        if request.user.is_authenticated:
            return render(request, "payment/billing_info.html",{"cart_products":cart_products, "quantities":quantities, "totals":totals, "shipping_info":request.POST })   
                
        else:
            pass
    else:
        messages.success(request, "")
        return redirect('home')

        





def checkout(request):
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()
    return render(request, "payment/checkout.html",{"cart_products":cart_products, "quantities":quantities, "totals":totals })
    