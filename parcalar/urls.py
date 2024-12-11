from django.urls import path
from . import views

urlpatterns = [
    path('', views.parca_listesi, name='parca_listesi'),
    path('ekle/', views.parca_ekle, name='parca_ekle'),
    path('guncelle/<int:id>/', views.parca_guncelle, name='parca_guncelle'),
    path('sil/<int:id>/', views.parca_sil, name='parca_sil'),
]
