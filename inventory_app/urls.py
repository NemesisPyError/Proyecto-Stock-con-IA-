from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, WarehouseViewSet, InventoryViewSet, StockMovementViewSet, ProductRequestViewSet
from inventory_app.admin_dashboard import resumen_agente_ia

router = DefaultRouter()
router.register("products", ProductViewSet)
router.register("warehouses", WarehouseViewSet)
router.register("inventories", InventoryViewSet, basename="inventory")
router.register("movements", StockMovementViewSet)
router.register("requests", ProductRequestViewSet)

urlpatterns = [
    path('', resumen_agente_ia, name='home'),
    path('api/', include(router.urls)),
]
