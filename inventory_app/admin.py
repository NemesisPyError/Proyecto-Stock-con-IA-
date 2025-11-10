from django.contrib import admin
from .models import Product, Warehouse, Inventory, StockMovement, ProductRequest

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("sku", "name","price", "reorder_point", "reorder_quantity")

@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ("name", "location")

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ("product", "warehouse", "quantity",  "last_counted")

@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ("product", "warehouse", "change", "movement_type", "created_at")

@admin.register(ProductRequest)
class ProductRequestAdmin(admin.ModelAdmin):
    list_display = ("product", "warehouse", "quantity_requested", "status", "requested_by", "created_at")