from django.contrib import admin
from .models import Membre, Tontine, Participation, Cotisation , DemandeAdhesion, MembreTontine

class ReadOnlyAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return request.user.groups.filter(name='Gestionnaires').exists()

    def has_change_permission(self, request, obj=None):
        return request.user.groups.filter(name='Gestionnaires').exists()

    def has_delete_permission(self, request, obj=None):
        return request.user.groups.filter(name='Gestionnaires').exists()


@admin.register(Membre)
class MembreAdmin(admin.ModelAdmin):
    list_display = ('nom', 'email', 'role', 'date_inscription')
    search_fields = ('nom', 'email')
    list_filter = ('role',)

@admin.register(Tontine)
class TontineAdmin(admin.ModelAdmin):
    list_display = ('nom', 'montant_cotisation', 'frequence_cotisation', 'date_debut', 'date_fin', 'gestionnaire')
    search_fields = ('nom',)
    list_filter = ('frequence_cotisation',)

@admin.register(Participation)
class ParticipationAdmin(admin.ModelAdmin):
    list_display = ('membre', 'tontine', 'date_adhesion')
    search_fields = ('membre__nom', 'tontine__nom')
    list_filter = ('date_adhesion',)

@admin.register(Cotisation)
class CotisationAdmin(admin.ModelAdmin):
    list_display = ('membre', 'tontine', 'montant', 'date_paiement')
    search_fields = ('membre__nom', 'tontine__nom')
    list_filter = ('date_paiement',)

    def has_add_permission(self, request):
        try:
            return request.user.is_superuser or request.user.membre.role == 'gestionnaire'
        except:
            return False

    def has_change_permission(self, request, obj=None):
        try:
            return request.user.is_superuser or request.user.membre.role == 'gestionnaire'
        except:
            return False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
    
@admin.register(DemandeAdhesion)
class DemandeAdhesionAdmin(admin.ModelAdmin):
    list_display = ['user', 'tontine', 'approuvee', 'date_demande']
    list_filter = ['approuvee', 'tontine']
    search_fields = ['user__username', 'tontine__nom']

    # Empêcher l'utilisateur de modifier après la création
    def has_change_permission(self, request, obj=None):
        if not request.user.is_superuser and obj:
            return False
        return True

    # Cacher le champ "user" dans le formulaire (auto-assigné)
    def get_fields(self, request, obj=None):
        if request.user.is_superuser:
            return ['user', 'tontine', 'approuvee']
        return ['tontine']

    # Auto-remplir le champ user à la sauvegarde
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.user = request.user  # assigner automatiquement l'utilisateur connecté

        # Si un admin approuve la demande
        if obj.approuvee and not MembreTontine.objects.filter(user=obj.user, tontine=obj.tontine).exists():
            MembreTontine.objects.create(user=obj.user, tontine=obj.tontine)

        super().save_model(request, obj, form, change)

    # Empêcher les membres simples d’approuver eux-mêmes
    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return ['approuvee']
        return []
@admin.register(MembreTontine)
class MembreTontineAdmin(admin.ModelAdmin):
    list_display = ['user', 'tontine', 'date_adhesion']
    list_filter = ['tontine']
    search_fields = ['user__username']

    

