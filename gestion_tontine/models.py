from django.db import models
class Tontine(models.Model):
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    members = models.IntegerField()

    def __str__(self):
        return self.name


class Membre(models.Model):
    nom = models.CharField(max_length=100)
    email = models.EmailField()
    date_naissance = models.DateField()
    montant_contribue = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Relation un à plusieurs (One-to-Many) : Un membre appartient à une tontine
    tontine = models.ForeignKey(Tontine, on_delete=models.CASCADE, related_name='membres')
    
    def __str__(self):
        return self.nom


class Participation(models.Model):
    membre = models.ForeignKey(Membre, on_delete=models.CASCADE)
    tontine = models.ForeignKey(Tontine, on_delete=models.CASCADE)
    date_adhesion = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.membre} dans {self.tontine}"

class Cotisation(models.Model):
    membre = models.ForeignKey(Membre, on_delete=models.CASCADE)
    tontine = models.ForeignKey(Tontine, on_delete=models.CASCADE)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    date_paiement = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.membre.nom} a payé {self.montant} FCFA"    
