from django.shortcuts import redirect
from user.models import User

def get_logged_in_user(request):
    if 'user_id' not in request.session:
        return redirect('login')  # Redirect to login if user_id is not in session
    
    user_id = request.session['user_id']
    try:
        user = User.objects.get(id=user_id)
        return user
    except User.DoesNotExist:
        return redirect('login')  # Redirect if user does not exist
