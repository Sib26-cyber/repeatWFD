
from django.contrib import admin
from django.urls import path,include
from . import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls')),  # Include URLs from the store app   
    

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Serve media files in development