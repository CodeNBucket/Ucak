from django.contrib import admin
from django.contrib.auth.hashers import make_password
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'takim')
    list_filter = ('takim',)
    search_fields = ('username',)

    def save_model(self, request, obj, form, change):
        # Hash the password if it's not already hashed
        if not obj.password.startswith('pbkdf2_sha256$'):
            obj.password = make_password(obj.password)
        super().save_model(request, obj, form, change)
