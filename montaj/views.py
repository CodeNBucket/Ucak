from django.shortcuts import render, get_object_or_404, redirect
from ucaklar.models import Ucak
from parcalar.models import Parca
from django.contrib.auth.decorators import login_required
from montaj.models import Montaj


@login_required
def eksik_parca_kontrol(request, ucak_id):
    ucak = get_object_or_404(Ucak, id=ucak_id)
    gerekli_parcalar = ['KANAT', 'GOVDE', 'KUYRUK', 'AVIYONIK']  # Gereken parça türleri
    mevcut_parcalar = Parca.objects.filter(ucak=ucak, stok__gt=0)  # Stokta olan parçalar

    eksik_parcalar = [tur for tur in gerekli_parcalar if not mevcut_parcalar.filter(tur=tur).exists()]
    if eksik_parcalar:
        return render(request, 'error.html', {'error': f'Bu parçalar eksik: {", ".join(eksik_parcalar)}'})
    
    return redirect('montaj_yap', ucak_id=ucak.id)


@login_required
def montaj_yap(request, ucak_id):
    ucak = get_object_or_404(Ucak, id=ucak_id)
    personel = request.user.personel

    # Sadece montaj takımı montaj yapabilir
    if personel.takim.takim_tipi != 'MONTAJ':
        return render(request, 'error.html', {'error': 'Montaj yapma yetkiniz yok.'})

    gerekli_parcalar = ['KANAT', 'GOVDE', 'KUYRUK', 'AVIYONIK']
    mevcut_parcalar = Parca.objects.filter(ucak=ucak, stok__gt=0)

    # Eksik parçaları kontrol et
    eksik_parcalar = [tur for tur in gerekli_parcalar if not mevcut_parcalar.filter(tur=tur).exists()]
    if eksik_parcalar:
        return render(request, 'error.html', {'error': f'Bu parçalar eksik: {", ".join(eksik_parcalar)}'})

    # Montaj işlemi
    montaj = Montaj.objects.create(ucak=ucak, takim=personel.takim)
    for parca in mevcut_parcalar:
        parca.stok -= 1  # Stoktan düş
        parca.save()
        montaj.kullanilan_parcalar.add(parca)  # Montaj ile ilişkilendir

    return render(request, 'success.html', {'message': f'{ucak.isim} başarıyla monte edildi.'})