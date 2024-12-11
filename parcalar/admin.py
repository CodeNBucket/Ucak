from django.contrib import admin
from .models import Parca

@admin.register(Parca)
class ParcaAdmin(admin.ModelAdmin):
    list_display = ('kategori', 'tur', 'ucak', 'takim', 'stok')  # Admin görünümü
    list_filter = ('tur', 'takim', 'ucak')  # Filtre seçenekleri
    search_fields = ('isim',)  # Arama yapılabilir alanlar
