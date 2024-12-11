from django.contrib import admin
from .models import Ucak

@admin.register(Ucak)
class UcakAdmin(admin.ModelAdmin):
    list_display = ('isim',)  # Admin görünümünde isim göster
    search_fields = ('isim',)  # İsimde arama yapmayı sağla
