from django.urls import path
from . import views

urlpatterns = [
   
    path('payment_success', views.payment_success, name='payment_success'),  # payment success page
     
    path('checkout', views.checkout, name='checkout'),  # checkout
    
    
    
]   
