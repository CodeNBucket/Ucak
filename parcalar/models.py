from django.db import models
from ucaklar.models import Ucak
from takimlar.models import Takim

class Parca(models.Model):
    # Parça türleri
    PARCA_TIPLERI = [
        ('SOLKANAT', 'Sol Kanat'),  # Left Wing
        ('SAGKANAT', 'Sağ Kanat'),  # Right Wing
        ('GOVDE', 'Gövde'),         # Body
        ('KUYRUK', 'Kuyruk'),       # Tail
        ('AVIYONIK', 'Aviyonik'),   # Avionics
    ]

    KATEGORI_TIPLERI = [
        ('TB2', 'TB2'),
        ('TB3', 'TB3'),
        ('AKINCI', 'Akıncı'),
        ('KIZILELMA', 'Kızıl Elma'),
    ]

    # Parçanın adı
    isim = models.CharField(max_length=150, blank=True)  # Parça ismi, örneğin "Sol Kanat TB2"
    
    # Parçanın ait olduğu kategori (örneğin: TB2, TB3)
    kategori = models.CharField(max_length=50, choices=KATEGORI_TIPLERI)  
    
    # Parçanın türü (Sol Kanat, Sağ Kanat, Gövde, vb.)
    tur = models.CharField(max_length=50, choices=PARCA_TIPLERI)
    
    # Parçanın ait olduğu takım (Örneğin: Montaj, Üretim)
    takim = models.ForeignKey(Takim, on_delete=models.CASCADE)
    
    # Parçanın stok miktarı
    stok = models.PositiveIntegerField(default=0)
    
    # Parçanın kullanılıp kullanılmadığı durumu
    kullanildi = models.BooleanField(default=False)
    
    # Parçanın kullanıldığı uçak
    ucak = models.ForeignKey(Ucak, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.isim} - {self.kategori} - {self.tur} ({'Kullanıldı' if self.kullanildi else 'Kullanılmadı'})"
    
    @classmethod
    def check_part_availability(cls, part_type, aircraft_type):
        """
        Kontrol eder, belirtilen tipteki parçaların yeterli olup olmadığını.
        Belirtilen uçak tipi için (Örneğin: TB2, AKINCI) envanterde parça olup olmadığı kontrol edilir.
        """
        try:
            part = cls.objects.get(tur=part_type, kategori=aircraft_type)
            return part.stok > 0  # Stok 0'dan büyükse True döndürür
        except cls.DoesNotExist:
            return False  # Eğer parça yoksa False döndürür
