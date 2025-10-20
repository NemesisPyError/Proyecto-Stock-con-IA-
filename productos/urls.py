from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from productos.views import ProductoViewSet  # <- IMPORTANTE

router = routers.DefaultRouter()
router.register(r'productos', ProductoViewSet)  # <- registrar el ViewSet

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),  # <- incluir las rutas del router
]
