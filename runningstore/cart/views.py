from django.shortcuts import render, get_object_or_404
from.cart import Cart
from store.models import Product
from django.http import JsonResponse
from django.contrib import messages

# Create your views here.
def cart_summary(request):
   #Get the cart
   cart=Cart(request)
   cart_products = cart.get_prods
   quantities = cart.get_quants
   totals = cart.cart_total()
   return render(request, "cart_summary.html",{ "cart_products":cart_products, "quantities":quantities, "totals":totals })





def cart_add(request):
    #Get the Cart
    cart = Cart(request)
    #test for POST
    if request.POST.get('action')=='post':
        #GET STUFF
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        #lookup product in DB
        product = get_object_or_404(Product, id=product_id)

        #Save to a Session
        cart.add(product=product, quantity = product_qty)
        #GET Cart QTY
        cart_quantity = cart.__len__()

        #Return a response
        response = JsonResponse({'qty':cart_quantity})
        messages.success(request, "Product added to cart")
        return response
        location.reload();

   




def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action')=='post':
        product_id = str(request.POST.get('product_id'))
        
        #lookup product in DB

        #Update the session cart
        cart.delete(product=product_id)
        #Get the cart qty
        
        response = JsonResponse ({'product_id':product_id})
        messages.success(request, "Product removed from cart")
        return response




def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action')=='post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        #lookup product in DB

        #Update the session cart
        cart.update(product=product_id, quantity=product_qty)
        #Get the cart qty
        
        response = JsonResponse({'qty':product_qty})
        messages.success(request, "Cart updated")   
        return response
        #return redirect("cart:summary")
