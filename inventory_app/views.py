from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Product, Warehouse, Inventory, StockMovement, ProductRequest
from .serializers import ProductSerializer, WarehouseSerializer, InventorySerializer, StockMovementSerializer, ProductRequestSerializer
from django.db.models import F

# Aquí se pueden definir vistas adicionales para usuarios no técnicos o para mostrar reportes fuera del admin.
# Ideal para crear interfaces más visuales o públicas.

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class WarehouseViewSet(viewsets.ModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer

class InventoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Inventory.objects.select_related("product", "warehouse").all()
    serializer_class = InventorySerializer

    @action(detail=False, methods=["get"])
    def low_stock(self, request):
        low = Inventory.objects.filter(quantity__lte=F('product__reorder_point')).select_related("product", "warehouse")
        serializer = self.get_serializer(low, many=True)
        return Response(serializer.data)

class StockMovementViewSet(viewsets.ModelViewSet):
    queryset = StockMovement.objects.all().order_by("-created_at")
    serializer_class = StockMovementSerializer

class ProductRequestViewSet(viewsets.ModelViewSet):
    queryset = ProductRequest.objects.all().order_by("-created_at")
    serializer_class = ProductRequestSerializer

