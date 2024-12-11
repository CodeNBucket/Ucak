from django.shortcuts import render, redirect, get_object_or_404
from .models import Takim

# Takım Listesi
def takim_listesi(request):
    takimlar = Takim.objects.all()
    return render(request, 'takimlar/takim_listesi.html', {'takimlar': takimlar})

# Takım Ekle
def takim_ekle(request):
    if request.method == 'POST':
        isim = request.POST['isim']
        takim_tipi = request.POST['takim_tipi']
        Takim.objects.create(isim=isim, takim_tipi=takim_tipi)
        return redirect('takim_listesi')
    return render(request, 'takimlar/takim_formu.html', {'is_ekle': True})

# Takım Güncelle
def takim_guncelle(request, id):
    takim = get_object_or_404(Takim, id=id)
    if request.method == 'POST':
        takim.isim = request.POST['isim']
        takim.takim_tipi = request.POST['takim_tipi']
        takim.save()
        return redirect('takim_listesi')
    return render(request, 'takimlar/takim_formu.html', {'takim': takim, 'is_ekle': False})

# Takım Sil
def takim_sil(request, id):
    takim = get_object_or_404(Takim, id=id)
    if request.method == 'POST':
        takim.delete()
        return redirect('takim_listesi')
    return render(request, 'takimlar/takim_sil_onay.html', {'takim': takim})
