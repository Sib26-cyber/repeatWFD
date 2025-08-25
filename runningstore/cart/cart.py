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


    def cart_total(self):
         #get the productIDs
        product_ids = self.cart.keys()
        #Use ids to lookup products in the database model
        products = Product.objects.filter(id__in=product_ids)
        quantities = self.cart
        #start with zero
        total = 0
        for key, value in quantities.items():
            #convert key string into an integer
            key = int(key)
            for product in products:
                if product.id == key:
                    key = int(key)
                    price = product.sale_price if product.sale_price else product.price
                    total += price * value
                    return total
                
                
    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)

        #Logic
        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = int (product_qty)
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
    
    def get_quants(self):
            quantities = self.cart
            return quantities
    
    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)

        ourcart = self.cart
        
        ourcart[product_id] = product_qty
        self.session.modified = True

        thing = self.cart
        return thing
    

    def delete(self, product):
        product_id = str(product)
        #delete the item from the cart(dictionary)
        if product_id in self.cart:
            del self.cart[product_id]
        self.session.modified = True
    