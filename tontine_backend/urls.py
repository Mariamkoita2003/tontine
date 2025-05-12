from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('gestion_tontine/', include('gestion_tontine.urls')),  # Ceci inclut les URL de gestion_tontine
]
