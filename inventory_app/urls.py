from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, WarehouseViewSet, InventoryViewSet, StockMovementViewSet, ProductRequestViewSet
from django.contrib import admin
from django.urls import path, include

router = DefaultRouter()
router.register("products", ProductViewSet)
router.register("warehouses", WarehouseViewSet)
router.register("inventories", InventoryViewSet, basename="inventory")
router.register("movements", StockMovementViewSet)
router.register("requests", ProductRequestViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("inventory_app.urls")),
]
