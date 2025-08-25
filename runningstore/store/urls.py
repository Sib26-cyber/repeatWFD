from django.urls import path
from . import views

urlpatterns = [
   
    path('', views.home, name='home'),  # Home page
    path('about/', views.about, name='about'),  # About page
    path('login/', views.login_user, name='login'),  # Login page
    path('logout/', views.logout_user, name='logout'),  # Logout page
    path('register/', views.register_user, name='register'), 
    path('update_password/', views.update_password, name='update_password'),  # password change page
    path('update_user/', views.update_user, name='update_user'),  # Update user page
    path('product/<int:pk>/', views.product, name='product'),  # Product page
    path('category/<str:foo>/', views.category, name='category'),  # Category page
    path('category_summary/',views.category_summary, name='category_summary'),
    path('update_info/', views.update_info, name='update_info'),  # Update profile page info
    path('items/', views.item_list, name='item_list'),  # Item list page    
    
    
    
]   
