from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.utils import timezone

class Membre(models.Model):
    ROLE_CHOICES = [
        ('membre', 'Membre'),
        ('gestionnaire', 'Gestionnaire'),
        ('super_admin', 'Super Administrateur'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profil')
    nom = models.CharField(max_length=100)
    email = models.EmailField()
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='membre')
    date_inscription = models.DateTimeField(default=timezone.now)
    
    @property
    def montant_contribue(self):
        total = self.cotisations.aggregate(Sum('montant'))['montant__sum'] or 0
        return total
    
    def __str__(self):
        return f"{self.nom} ({self.get_role_display()})"

class Tontine(models.Model):
    FREQUENCE_CHOICES = [
        ('quotidien', 'Quotidien'),
        ('hebdomadaire', 'Hebdomadaire'),
        ('mensuel', 'Mensuel'),
    ]
    
    nom = models.CharField(max_length=100)
    description = models.TextField(default="Pas de description")
    montant_cotisation = models.DecimalField(max_digits=10, decimal_places=2)
    frequence_cotisation = models.CharField(max_length=20, choices=FREQUENCE_CHOICES, default='mensuel')
    date_debut = models.DateField(default=timezone.now)  # Valeur par défaut
    date_fin = models.DateField(null=True, blank=True)
    gestionnaire = models.ForeignKey(Membre, on_delete=models.CASCADE, related_name='tontines_gerees')
    
    def __str__(self):
        return self.nom
    
    def afficher_membres(self):
        return ", ".join([membre.nom for membre in self.participants.all()])

class Participation(models.Model):
    membre = models.ForeignKey(Membre, on_delete=models.CASCADE, related_name='participations')
    tontine = models.ForeignKey(Tontine, on_delete=models.CASCADE, related_name='participants')
    date_adhesion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('membre', 'tontine')
    
    def __str__(self):
        return f"{self.membre.nom} - {self.tontine.nom}"

class Cotisation(models.Model):
    membre = models.ForeignKey(Membre, on_delete=models.CASCADE, related_name='cotisations')
    tontine = models.ForeignKey(Tontine, on_delete=models.CASCADE, related_name='cotisations')
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    date_paiement = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.membre.nom} - {self.tontine.nom} - {self.montant} € - {self.date_paiement.strftime('%d/%m/%Y')}"
