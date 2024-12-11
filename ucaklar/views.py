from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404

from parcalar.models import Parca
from user.helpers import get_logged_in_user
from .models import Ucak



def ucak_ekle(request):
    """Yeni uçak ekle."""
    user = get_logged_in_user(request)
    if isinstance(user, HttpResponseRedirect):
        return user

    # Eğer kullanıcı Montaj takımı değilse, dashboard'a geri döndür
    if user.takim.takim_tipi != 'MONTAJ':
        return redirect('dashboard')

    if request.method == 'POST':
        isim = request.POST['isim']
        kategori = request.POST['kategori']
        selected_parts = request.POST.getlist('parts')  # Seçilen parçaların ID'lerini al

        # Kategoriyi kontrol et ve parçaları grupla
        required_parts = {
            'GOVDE': 1,   # 1 adet Gövde
            'SOLKANAT': 1,  # 1 adet Sol Kanat
            'SAGKANAT': 1,  # 1 adet Sağ Kanat
            'AVIYONIK': 1, # 1 adet Aviyonik
            'KUYRUK': 1   # 1 adet Kuyruk
        }

        # Stok kontrolü yapalım
        part_counts = {
            'GOVDE': 0,
            'SOLKANAT': 0,
            'SAGKANAT': 0,
            'AVIYONIK': 0,
            'KUYRUK': 0
        }

        # Seçilen parçalarla stok kontrolü yap
        for part_id in selected_parts:
            part = Parca.objects.get(id=part_id)
            if part.kategori == kategori:  # Seçilen parça kategorisiyle eşleşiyor mu?
                part_counts[part.tur] += 1

        # Eksik parça kontrolü
        missing_parts = []
        for part_type, required_count in required_parts.items():
            if part_counts[part_type] < required_count:
                missing_parts.append(f"{part_type} parçası eksik")

        # Eksik parça varsa hata mesajı ver
        if missing_parts:
            return render(request, 'ucaklar/hata.html', {'error': 'Eksik parça(lar): ' + ', '.join(missing_parts)})

        # Uçak oluşturuluyor
        ucak = Ucak.objects.create(isim=isim, model=kategori)

        # Seçilen parçaları uçağa ata ve stoktan düşür
        for part_id in selected_parts:
            part = Parca.objects.get(id=part_id)
            part.ucak = ucak  # Parçayı uçağa ilişkilendir
            part.save()

            # Parça stoktan düş
            if part.tur == 'KANAT':
                part.stok -= 2  # Kanatlar için 2 adet düşürülmeli
            else:
                part.stok -= 1  # Diğer parçalar için 1 adet düşürülmeli

            part.save()

        return redirect('dashboard')

    # Kullanılabilir parçaları getir
    parts = Parca.objects.filter(stok__gt=0)  # Stokta bulunan parçalar
    return render(request, 'ucaklar/ucak_formu.html', {'parts': parts, 'user': user})
   



def ucak_listesi(request):
    """Uçakların listelendiği sayfa."""
    user = get_logged_in_user(request)
    if isinstance(user, HttpResponseRedirect):
        return user

    # Sadece montaj takımı uçağı görebilir
    if user.takim.takim_tipi != 'MONTAJ':
        return render(request, 'error.html', {'error': 'Bu işlem sadece Montaj takımına aittir.'})

    # Tüm uçakları getir
    ucaklar = Ucak.objects.all()
    return render(request, 'ucaklar/ucak_listesi.html', {'ucaklar': ucaklar})


def ucak_detay(request, ucak_id):
    """Uçağın detaylarını göster."""
    user = get_logged_in_user(request)
    if isinstance(user, HttpResponseRedirect):
        return user

    # Uçak ve ona bağlı parçaları getir
    ucak = get_object_or_404(Ucak, id=ucak_id)
    # Fetch the parts that belong to this aircraft
    parts = Parca.objects.filter(ucak=ucak)

    return render(request, 'ucaklar/ucak_detay.html', {'ucak': ucak, 'parts': parts})