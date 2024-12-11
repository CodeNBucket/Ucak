from django.contrib import admin
from .models import Montaj

@admin.register(Montaj)
class MontajAdmin(admin.ModelAdmin):
    list_display = ('ucak', 'tarih', 'takim')  # Fields to display in the admin list view
    list_filter = ('tarih', 'takim')          # Add filters for date and team
    search_fields = ('ucak__isim', 'takim__isim')  # Enable search by aircraft and team names
