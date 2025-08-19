
from django.contrib import admin
from django.urls import path,include
from . import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls')),  # Include URLs from the store app
<<<<<<< HEAD
    path('cart/', include('cart.urls')),
=======
    path('cart/', include ('cart.urls')),
>>>>>>> 74a904e076c8b1cf8ba50cb059003c81fef3ae82
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Serve media files in development