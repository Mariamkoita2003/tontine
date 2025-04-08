from django.contrib import admin
from .models import Tontine, Membre, Participation, Cotisation

admin.site.register(Tontine)
admin.site.register(Membre)
admin.site.register(Participation)
admin.site.register(Cotisation)

# Register your models here.
