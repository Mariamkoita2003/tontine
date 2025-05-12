# decorators.py
from django.shortcuts import redirect
from functools import wraps
from .models import Membre

def super_admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        try:
            membre = Membre.objects.get(user=request.user)
            if membre.role == 'super_admin':
                return view_func(request, *args, **kwargs)
            else:
                return redirect('access_denied')
        except Membre.DoesNotExist:
            return redirect('access_denied')
    return wrapper

def gestionnaire_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        try:
            membre = Membre.objects.get(user=request.user)
            if membre.role in ['gestionnaire', 'super_admin']:  # Super admin a aussi les droits du gestionnaire
                return view_func(request, *args, **kwargs)
            else:
                return redirect('access_denied')
        except Membre.DoesNotExist:
            return redirect('access_denied')
    return wrapper

def membre_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Tous les utilisateurs authentifiés sont au moins des membres
        if request.user.is_authenticated:
            try:
                Membre.objects.get(user=request.user)  # Vérifie que le profil existe
                return view_func(request, *args, **kwargs)
            except Membre.DoesNotExist:
                return redirect('access_denied')
        else:
            return redirect('login')
    return wrapper