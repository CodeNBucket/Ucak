from django.urls import path
from . import views

urlpatterns = [
    path('ucak/ekle/', views.ucak_ekle, name='ucak_ekle'),
    path('ucak/listesi/', views.ucak_listesi, name='ucak_listesi'),
    path('ucak/detay/<int:ucak_id>/', views.ucak_detay, name='ucak_detay'),  # Detay sayfası
]
