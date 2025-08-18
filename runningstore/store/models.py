from django.db import models
import datetime
from django.contrib.auth.models import User

from django.db.models.signals import post_save 


#Create customer profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(User, auto_now= True)
    phone = models.CharField(max_length=20, blank=True)
    address1 = models.CharField(max_length =200, blank=True)
    address2 = models.CharField(max_length =200, blank=True)
    city = models.CharField(max_length =200, blank=True)
    country = models.CharField(max_length =200, blank=True)

    def __str__(self):
        return self.user.username
    
#Create a user profile by default when user signs up
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
#Automate the profile
post_save.connect(create_profile, sender = User)






class Category(models.Model):
    
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Categories"
       
    
    
class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=500, blank=True, null=True)
    size = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    image = models.ImageField(upload_to='uploads/product/', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    stock = models.PositiveIntegerField(default=0)
    #add sale stock
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50,unique=True)
    password = models.CharField(max_length=50)  # Store hashed password
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

    
class Order(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE, max_length=200)
    customer_email = models.EmailField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=15,default= '', blank=True, null=True)
    payment_method = models.CharField(max_length=50, default='Credit Card')
    order_date = models.DateTimeField(default=datetime.datetime.now)
    status = models.BooleanField(max_length=50, default='False')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)


    def __str__(self):
        return f"Order by {self.customer_name} for {self.product.name}"
    


class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    refund_date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Refund for Order {self.order.id} - {self.reason[:50]}"
    
class Return(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    return_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='Pending')

    def __str__(self):
        return f"Return for Order {self.order.id} - {self.reason[:50]}"





# Create your models here.
