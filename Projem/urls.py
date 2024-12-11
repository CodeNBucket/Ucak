from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),  # Include the user app's URLs
    path('takimlar/', include('takimlar.urls')),  # Takım URL'leri
    path('parcalar/', include('parcalar.urls')),
    path('ucaklar/', include('ucaklar.urls')),
    path('montaj/', include('montaj.urls')),


]
