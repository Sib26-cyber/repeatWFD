
from django.contrib import admin
from django.urls import path,include
from . import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
<<<<<<< HEAD
    path('', include('store.urls')),# Include URLs from the store app
    path('cart/',include)
     
    

=======
    path('', include('store.urls')),  # Include URLs from the store app
<<<<<<< HEAD
    path('cart/', include('cart.urls')),
=======
    path('cart/', include ('cart.urls')),
>>>>>>> 74a904e076c8b1cf8ba50cb059003c81fef3ae82
>>>>>>> 979982e9cbdf43b65a18b999fe115e52e442886a
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Serve media files in development