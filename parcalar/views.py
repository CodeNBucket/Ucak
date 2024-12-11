from django.shortcuts import render, redirect, get_object_or_404
from .models import Parca
from ucaklar.models import Ucak
from user.helpers import get_logged_in_user  # Login kontrolü için helper function
from django.http import HttpResponseRedirect  # Redirect kontrolü için gerekli

def parca_listesi(request):
    """Takıma ait parçaları listele."""
    user = get_logged_in_user(request)  # Oturum kontrolü
    if isinstance(user, HttpResponseRedirect):  # Eğer yönlendirme dönerse
        return user

    # Kullanıcının takımına ait parçalar
    parcalar = Parca.objects.filter(takim=user.takim)   
    return render(request, 'parcalar/parca_listesi.html', {'parcalar': parcalar})

def parca_ekle(request):
    """Yeni parça ekle."""
    user = get_logged_in_user(request)
    if isinstance(user, HttpResponseRedirect):
        return user

    if request.method == 'POST':
        stok = request.POST['stok']
        kategori = request.POST['kategori']  # Updated to kategori
        isim = request.POST['isim']

        # Parça türünü takım türüne göre belirle
        takim_tipi = user.takim.takim_tipi
        if takim_tipi == 'URETIM':
            tur = request.POST['tur']
        else:
            tur = user.takim.takim_tipi  # Montaj takımıysa türü sabit tut

        # Parçayı ekle
        Parca.objects.create(kategori=kategori, tur=tur, takim=user.takim, stok=stok,isim=isim)
        return redirect('dashboard')

    return render(request, 'parcalar/parca_formu.html', {
        'user': user,  # Kullanıcı bilgilerini şablona geçir
        'ucaklar': Ucak.objects.all()  # Uçak seçim listesi
    })

def parca_guncelle(request, id):
    """Var olan parçayı güncelle."""
    user = get_logged_in_user(request)
    if isinstance(user, HttpResponseRedirect):
        return user

    parca = get_object_or_404(Parca, id=id)

    # Takım yetkisi kontrolü
    if parca.takim != user.takim:
        return render(request, 'error.html', {'error': 'Bu parçayı güncelleme yetkiniz yok.'})

    # Eğer kullanıcı 'URETIM' takımı ise tür sabit ve gösterilir
    if request.method == 'POST':
        stok = request.POST['stok']
        isim=request.POST['isim']
        kategori = request.POST['kategori']  # Updated to kategori

        # Güncelleme işlemi
        parca.kategori = kategori
        parca.stok = stok
        parca.isim= isim
        parca.save()
        return redirect('dashboard')

    return render(request, 'parcalar/parca_formu.html', {'parca': parca, 'user': user, 'is_ekle': False})

def parca_sil(request, id):
    """Parça sil."""
    user = get_logged_in_user(request)
    if isinstance(user, HttpResponseRedirect):
        return user

    parca = get_object_or_404(Parca, id=id)

    # Takım yetkisi kontrolü
    if parca.takim != user.takim:
        return render(request, 'error.html', {'error': 'Bu parçayı silme yetkiniz yok.'})

    if request.method == 'POST':
        parca.delete()
        return redirect('dashboard')
    return render(request, 'parcalar/parca_sil_onay.html', {'parca': parca})
