from django.contrib import admin
from .models import Category, Customer, Product, Order, Refund, Return  

# Register your models here.
admin.site.register(Category)
admin.site.register (Customer)
admin.site.register (Product)
admin.site.register (Order)
admin.site.register (Refund)
admin.site.register (Return)
  # Replace 'ModelName' with your actual model name
