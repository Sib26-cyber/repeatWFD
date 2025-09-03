
from django.contrib import admin
from django.urls import path,include
from . import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls')),# Include URLs from the store app      
    path('cart/', include('cart.urls')),
    path('payment/', include('payment.urls')), 
    path('returns/', include('returns.urls' , namespace= 'returns')),# Include URLs from the returns app
<<<<<<< HEAD
    path('payment/', include('payment.urls')),  # Include URLs from the payment app
    path('returns/', include('returns.urls')),
=======
    path('payment/', include('payment.urls')), 
    path('returns/', include('returns.urls' , namespace= 'returns')),# Include URLs from the returns app
>>>>>>> 839e68230ae948050700d740f40f0e57e0d317da

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Serve media files in development