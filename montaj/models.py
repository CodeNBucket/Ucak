from django.db import models
from takimlar.models import Takim
from ucaklar.models import Ucak

class Montaj(models.Model):
    ucak = models.OneToOneField(Ucak, on_delete=models.CASCADE, related_name="montaj")
    tarih = models.DateField(auto_now_add=True)
    takim = models.ForeignKey(Takim, on_delete=models.CASCADE) # related name ters ilişki için gerekli


    def __str__(self):
        return f"Montaj: {self.ucak.isim} ({self.tarih})"
