from collections import defaultdict
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from user.models import User
from django.contrib.auth.hashers import check_password
from user.helpers import get_logged_in_user
from django.http import HttpResponseRedirect
from parcalar.models import Parca
from takimlar.models import Takim

def login_view(request):
    # Eğer kullanıcı zaten giriş yaptıysa, login sayfasına gitmemelidir
    if 'user_id' in request.session:
        return redirect('dashboard')  # Giriş yaptıysa dashboard'a yönlendir

    if request.method == 'POST':
        username = request.POST['username'].strip()  # Whitespace'leri temizle
        password = request.POST['password']

        print(f"Attempting to log in with username: '{username}'")

        # Kullanıcıyı veritabanında ara
        try:
            user = User.objects.get(username__iexact=username)
        except User.DoesNotExist:
            print("No user found with that username")
            return render(request, 'user/login.html', {'error': 'User does not exist'})

        # Parolayı kontrol et
        if check_password(password, user.password):
            print("Password matched successfully!")

            # Kullanıcıyı giriş yapmış olarak işaretle
            request.session['user_id'] = user.id  # Custom User için session'ı manuel olarak sakla
            return redirect('dashboard')  # Başarıyla giriş yaptıysa dashboard'a yönlendir
        else:
            print("Password does not match")
            return render(request, 'user/login.html', {'error': 'Invalid username or password'})

    return render(request, 'user/login.html')


def dashboard_view(request):
    user = get_logged_in_user(request)
    if isinstance(user, HttpResponseRedirect):
        return user

    # Fetching the user's team's parts
    parcalar = Parca.objects.filter(takim=user.takim)
    takim_uyeleri = user.takim.uyeler.all()  # Takım üyelerini al

    # Fetching all parts and categorizing them by team
    all_parcalar = Parca.objects.all()
    kategorize_parcalar = {}

    for parca in all_parcalar:
        takim = parca.takim
        # Exclude the user's team
        if takim == user.takim:
            continue
        if takim not in kategorize_parcalar:
            kategorize_parcalar[takim] = []
        kategorize_parcalar[takim].append(parca)

    # If the user's team is 'URETIM', allow editing and adding parts
    can_edit_parts = user.takim.takim_tipi == 'URETIM'

    # Now pass 'kategorize_parcalar', 'parcalar', 'user', 'can_edit_parts' to the template
    return render(request, 'user/dashboard.html', {
        'user': user,
        'parcalar': parcalar,
        'kategorize_parcalar': kategorize_parcalar,
        'can_edit_parts': can_edit_parts,   
        'takim_uyeleri': takim_uyeleri
    })


def logout_view(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    return redirect('login')
