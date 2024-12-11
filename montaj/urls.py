from django.urls import path
from . import views

urlpatterns = [
    path('eksik-parca-kontrol/<int:ucak_id>/', views.eksik_parca_kontrol, name='eksik_parca_kontrol'),
    path('montaj-yap/<int:ucak_id>/', views.montaj_yap, name='montaj_yap'),
]
