from django.contrib import admin
from .models import Tontine, Membre, Participation, Cotisation


class TontineAdmin(admin.ModelAdmin):
    list_display = ('nom', 'montant_cotisation', 'afficher_membres', 'gestionnaire')
    search_fields = ('nom',)
    list_filter = ('montant_cotisation',)

class MembreAdmin(admin.ModelAdmin):
    list_display = ('nom', 'email', 'montant_contribue')
    search_fields = ('nom', 'email')
    list_filter = ('role',)  # Utilise "role" à la place de "montant_contribue"

class ParticipationAdmin(admin.ModelAdmin):
    list_display = ('membre', 'tontine', 'date_adhesion')
    list_filter = ('tontine', 'date_adhesion')

class CotisationAdmin(admin.ModelAdmin):
    list_display = ('membre', 'tontine', 'montant', 'date_paiement')
    list_filter = ('tontine', 'date_paiement')
    search_fields = ('membre__nom',)

# 🔥 Enregistrement avec les bons Admins personnalisés :
admin.site.register(Membre, MembreAdmin)
admin.site.register(Participation, ParticipationAdmin)
admin.site.register(Cotisation, CotisationAdmin)
admin.site.register(Tontine, TontineAdmin)
