from django.http import HttpResponse
from django.shortcuts import render
from .models import Tontine

def dashboard(request):
    return render(request, 'gestion_tontine/dashboard.html')
# Create your views here.
