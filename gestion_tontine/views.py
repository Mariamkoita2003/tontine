from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import DemandeAdhesion, Tontine

@login_required
def demander_adhesion(request):
    if request.method == "POST":
        tontine_id = request.POST.get("tontine_id")
        tontine = Tontine.objects.get(id=tontine_id)

        # Vérifie qu'une demande n'existe pas déjà
        if not DemandeAdhesion.objects.filter(utilisateur=request.user, tontine=tontine).exists():
            DemandeAdhesion.objects.create(utilisateur=request.user, tontine=tontine)

        return redirect("confirmation_demande")

    tontines = Tontine.objects.all()
    return render(request, "demander_adhesion.html", {"tontines": tontines})
