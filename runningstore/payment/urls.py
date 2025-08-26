from django.urls import path
from . import views

urlpatterns = [
   
    path('payment_success', views.payment_success, name='payment_success'),  # Home page
     # Request refund page
    
    
    
]   
