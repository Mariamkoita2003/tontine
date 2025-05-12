# views.py
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.shortcuts import render
from .forms import InscriptionForm
from django.db.models import Sum
from .models import Membre, Cotisation, Participation
from .models import Tontine 
from .forms import TontineForm
from django.http import HttpResponseForbidden
from .decorators import super_admin_required, gestionnaire_required, membre_required

   
def access_denied(request):
    return render(request, 'gestion_tontine/access_denied.html')
 
def inscription_view(request):
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirige vers la page de login après inscription
    else:
        form = InscriptionForm()
    
    return render(request, 'gestion_tontine/inscription.html', {'form': form})  
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()  # Authentifie l'utilisateur
            login(request, user)  # Connecte l'utilisateur
            return redirect('dashboard')  # Redirige vers le dashboard après la connexion
        else:
            return render(request, 'gestion_tontine/login.html', {'form': form, 'error': 'Nom d\'utilisateur ou mot de passe incorrect'})
    else:
        form = AuthenticationForm()

    return render(request, 'gestion_tontine/login.html', {'form': form})
from django.shortcuts import render

@login_required
def dashboard(request):
    try:
        membre = Membre.objects.get(user=request.user)
    except Membre.DoesNotExist:
        membre = None

    if membre:
        # Logic for gestionnaire dashboard
        if membre.role == 'gestionnaire':
            # Logique spécifique au gestionnaire
            total_cotise = Cotisation.objects.filter(membre=membre).aggregate(Sum('montant'))['montant__sum'] or 0
            cotisations = Cotisation.objects.filter(membre=membre).order_by('-date_paiement')[:3]
            participations = Participation.objects.filter(membre=membre)
            context = {
                'membre': membre,
                'total_cotise': total_cotise,
                'cotisations': cotisations,
                'participations': participations,
                'is_gestionnaire': True,  # Ajouter un indicateur pour le gestionnaire
            }
        else:
            # Logique spécifique au membre simple
            participations = Participation.objects.filter(membre=membre)
            context = {
                'membre': membre,
                'participations': participations,
                'is_gestionnaire': False,  # Indicateur pour membre simple
            }
    else:
        context = {}

    return render(request, 'gestion_tontine/dashboard.html', context)


def tontine_list(request):
    tontines = Tontine.objects.all()
    return render(request, 'gestion_tontine/tontine_list.html', {'tontines': tontines})


# Adhérer à une tontine (si connecté)
@login_required
def rejoindre_tontine(request, tontine_id):
    tontine = Tontine.objects.get(id=tontine_id)
    # Ici, on pourrait ajouter la logique pour inscrire l'utilisateur dans la tontine
    # Par exemple : 
    # Membre.objects.create(nom=user.username, email=user.email, tontine=tontine)
    return redirect('dashboard')  # Redirige vers le dashboard après l'adhésion
def creer_tontine(request):
    try:
        membre = Membre.objects.get(user=request.user)
    except Membre.DoesNotExist:
        return HttpResponseForbidden("Aucun profil de membre trouvé pour cet utilisateur.")
    
    # Vérifie que l'utilisateur est un gestionnaire
    if membre.role != 'gestionnaire':
        return HttpResponseForbidden("Vous n'êtes pas autorisé à créer une tontine.")
    
    if request.method == 'POST':
        form = TontineForm(request.POST)
        if form.is_valid():
            tontine = form.save(commit=False)
            tontine.gestionnaire = membre  # Associe le membre gestionnaire à la tontine
            tontine.save()
            return redirect('tontines_list')  # Redirige vers la liste des tontines après la création
    else:
        form = TontineForm()

    return render(request, 'gestion_tontine/creer_tontine.html', {'form': form})

def gestion_utilisateurs(request):
    return render(request, 'gestion_tontine/gestion_utilisateurs.html')

def gestion_tontines(request):
    return render(request, 'gestion_tontine/gestion_tontines.html')


def consulter_tontines(request):
    return render(request, 'gestion_tontine/consulter_tontines.html')
