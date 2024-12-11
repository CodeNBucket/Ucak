from django.contrib import admin
from .models import Takim

@admin.register(Takim)
class TakimAdmin(admin.ModelAdmin):
    list_display = ('isim', 'takim_tipi')  # Admin panelinde isim ve türü göster
    list_filter = ('takim_tipi',)         # Takım tipine göre filtreleme ekle
    search_fields = ('isim',)            # İsim alanında arama yapmayı sağla
