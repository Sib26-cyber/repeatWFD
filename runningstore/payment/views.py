from django.shortcuts import render, redirect
from cart.cart import Cart
from django.contrib import messages
from payment.models import ShippingAddress,Order, OrderItem
from payment.forms import ShippingForm, PaymentForm
from django.contrib.auth.models import User
from store.models import Product



# Create your views here.
def payment_success(request):
    return render(request, 'payment/payment_success.html', {})



def billing_info(request):    
    if request.POST:         
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()
        #create a Session to hold shipping info
        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping

        #Check if user is authenticated
        if request.user.is_authenticated: 
            #Get the Billing info of the user
            billing_form = PaymentForm()           
            return render(request, "payment/billing_info.html",{"cart_products":cart_products,
                                 "quantities":quantities, "totals":totals, "shipping_info":request.POST, "billing_form":billing_form })
            
        else:
                billing_form = PaymentForm()
                return render(request, "payment/billing_info.html",{"cart_products":cart_products,
                                 "quantities":quantities, "totals":totals, "shipping_info":request.POST, "billing_form":billing_form })               
        
        shipping_form = request.POST
        return render(request, "payment/billing_info.html",{"cart_products":cart_products,
                                 "quantities":quantities, "totals":totals, "shipping_info":request.POST })
    else:
        messages.success(request, "Access Denied!")
        return redirect('home') 
                                  

      
def checkout(request):
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()

    if request.user.is_authenticated:
        shipping_user = ShippingAddress.objects.get(shipping_user__id=request.user.id)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        return render(request, "payment/checkout.html",{"cart_products":cart_products, "quantities":quantities, "totals":totals, "shipping_form":shipping_form })
       
    else:
        shipping_form = ShippingForm(request.POST or None)            
        return render(request, "payment/checkout.html",{"cart_products":cart_products, "quantities":quantities, "totals":totals })
                   
def process_order(request):
         if request.POST:
            #Get cart details
            cart = Cart(request)
            cart_products = cart.get_prods
            quantities = cart.get_quants
            totals = cart.cart_total()

            payment_form = PaymentForm(request.POST or None)
            #Get shipping session data
            my_shipping = request.session.get('my_shipping')
            #Create Shipping Address from session data
            full_name = my_shipping['shipping_full_name']
            email = my_shipping['shipping_email']
            amount_paid = totals

            shipping_address = f"{my_shipping['shipping_address_line1']}\n {my_shipping['shipping_address_line2']}\n {my_shipping['shipping_city']}\n {my_shipping['shipping_state']}\n {my_shipping['shipping_postal_code']}\n{my_shipping['shipping_country']}"
            #Get cart details
            user = request.user if request.user.is_authenticated else None
            create_order = Order.objects.create(user=user, full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()
            
            #Create Order Items
            order_id = create_order.pk
            quants = quantities() if callable(quantities) else quantities
            for product in cart_products():
                #get product id 
                product_id = product.id
                #get product price
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price
                    
                for key, value in quants.items():
                    if int(key) == product.id:                               
            
            
            
            
            
                        Create_order_item = OrderItem.objects.create(order_id=order_id, product_id=product_id, user = user, quantity=value, price=price)
                        Create_order_item.save() 
            #Deleting the Cart
            for key in list(request.session.keys()):
                if key =="session_key":
                    del request.session[key]                                                     
                                      
                
            messages.success(request, "Order Processed Successfully!")
            return redirect('home')     
            
        
         else:             
            #not logged in 
            create_order = Order.objects.create( full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()
            messages.success(request, "not logged in ")
            return redirect('home')            
                        
                        #create order item
                   
            
                
                
            
            
        
        
        
        
        
        
        
            
        
            
             
                           
                                                 
            


        
        
        

        





