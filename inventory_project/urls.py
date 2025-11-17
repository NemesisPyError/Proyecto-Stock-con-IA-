

# Define las rutas principales del proyecto.
# Incluye el panel de administración y la vista personalizada del resumen del agente IA.
from django.contrib import admin
from django.urls import path, include
from inventory_app.admin_dashboard import resumen_agente_ia

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/resumen-agente-ia/', resumen_agente_ia, name='resumen_agente_ia'),

    # incluye todas las rutas de inventory_app
    path('', include('inventory_app.urls')),
]
