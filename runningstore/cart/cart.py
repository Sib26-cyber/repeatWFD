from store.models import Product


class Cart():
    def __init__(self, request):
        self.session = request.session

#Get the current session key if it exists
        cart = self.session.get('session_key')
    #if the user is new, no session key! Create one
        if 'session_key' not in request.session:
            cart = self.session['session_key']={}

    #Make sure cart is available on all pages of the site
        self.cart = cart
    def add(self, product):
        product_id = str(product.id)

        #Logic
        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = {'price': str(product.price)}
        self.session.modified = True

        #counts the items in the cart 
    def __len__(self):
        return len(self.cart)
        #Look up products and add to the summary page

    def get_prods(self):
             product_ids = self.cart.keys()
             #Use ids to lookup products in the database model
             products = Product.objects.filter(id__in=product_ids)
             #Return the products that were looked up
             return products
