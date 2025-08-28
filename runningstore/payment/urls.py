from django.urls import path
from . import views



urlpatterns = [
   
    path('payment_success', views.payment_success, name='payment_success'),  # payment success page
    path('billing_info', views.billing_info, name='billing_info'),  # billing info page
    path('checkout', views.checkout, name='checkout'),  # checkout
    path('process_order', views.process_order, name='process_order'),  # process order
    
    
    
]   
