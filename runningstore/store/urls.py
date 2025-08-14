from django.urls import path
from . import views

urlpatterns = [
   
    path('', views.home, name='home'),  # Home page
    path('about/', views.about, name='about'),  # About page
    path('login/', views.login_user, name='login'),  # Login page
    path('logout/', views.logout_user, name='logout'),  # Logout page
    path('register/', views.register_user, name='register'),  # Registration page
<<<<<<< HEAD
    path('product/<int:pk>/', views.product, name='product'),  # Product page)
=======
    path('product/<int:pk>/', views.product, name='product'),  # Product detail page
>>>>>>> 3371a0938f88fcd24974325caa10873009ee2975
]
