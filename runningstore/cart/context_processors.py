from.cart import Cart

#Create context_processor so our cart can work on all pages of the site
def cart(request):
    #return the default data from the cart
    return{'cart':Cart( request)}
