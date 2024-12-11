from django.db import models
from django.core.exceptions import ValidationError

class Takim(models.Model):
    TAKIM_TIPLERI = [
        ('URETIM', 'Üretim Takımı'),
        ('MONTAJ', 'Montaj Takımı'),
    ]

    TUR_TIPLERI = [
        ('KANAT', 'Kanat'),
        ('GOVDE', 'Gövde'),
        ('AVIYONIK', 'Aviyonik'),
        ('KUYRUK', 'Kuyruk'),
    ]

    isim = models.CharField(max_length=150, unique=True)
    takim_tipi = models.CharField(max_length=50, choices=TAKIM_TIPLERI)
    tur = models.CharField(max_length=50, choices=TUR_TIPLERI, blank=True, null=True)

    def clean(self):
        """Custom validation for 'tur' field."""
        if self.takim_tipi == 'URETIM' and not self.tur:
            raise ValidationError("Tur field is required when Takim Tipi is 'URETIM'")

    def save(self, *args, **kwargs):
        """Override save to clean data before saving."""
        self.full_clean()  # Ensure that custom validation is called before saving
        super().save(*args, **kwargs)

    def __str__(self):
        return self.isim
