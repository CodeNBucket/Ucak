from django.db import models
from django.utils.timezone import now
from takimlar.models import Takim  # Takim modelini import ediyoruz

class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=150)  # Şifreler hashli olarak saklanır
    takim = models.ForeignKey(Takim, on_delete=models.CASCADE, related_name="uyeler")  # ForeignKey field

    def save(self, *args, **kwargs):
        # Hash the password only if it's not already hashed
        if not self.password.startswith('pbkdf2_sha256$'):
            from django.contrib.auth.hashers import make_password
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username