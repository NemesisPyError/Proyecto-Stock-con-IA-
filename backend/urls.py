# backend/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from productos.views import ProductoViewSet

# Creamos el router y registramos el ViewSet
router = routers.DefaultRouter()
router.register(r'productos', ProductoViewSet, basename='producto')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),  # La API estará en /api/productos/
]
