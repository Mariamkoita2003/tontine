# forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Tontine, Membre

class InscriptionForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True, label='Prénom')
    last_name = forms.CharField(required=True, label='Nom')
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(InscriptionForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            # Création automatique d'un profil membre pour chaque utilisateur inscrit
            Membre.objects.create(
                user=user,
                nom=f"{user.first_name} {user.last_name}",
                email=user.email,
                role='membre'  # Rôle par défaut
            )
        
        return user

class TontineForm(forms.ModelForm):
    class Meta:
        model = Tontine
        fields = ['nom', 'description', 'montant_cotisation', 'frequence_cotisation', 'date_debut', 'date_fin']
        widgets = {
            'date_debut': forms.DateInput(attrs={'type': 'date'}),
            'date_fin': forms.DateInput(attrs={'type': 'date'}),
        }