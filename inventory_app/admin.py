from django.contrib import admin
from .models import Product, Warehouse, Inventory, StockMovement, ProductRequest
from .llm_agent import revisar_stock_y_generar_solicitudes, aprobar_solicitudes_automaticamente
from django.utils.html import format_html
from django.urls import reverse

# Personaliza el panel de administración de Django para cada modelo.
# Agrega acciones personalizadas como “Ejecutar agente IA” y muestra el estado del stock con íconos o etiquetas.

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ("product", "warehouse", "quantity", "last_counted", "stock_status")
    list_filter = ("warehouse",)
    search_fields = ("product__name", "warehouse__name")
    actions = ["ejecutar_agente_ia"]

    def stock_status(self, obj):
        if obj.quantity <= obj.product.reorder_point:
            return " Bajo"
        return " OK"
    stock_status.short_description = "Estado de stock"

    def ejecutar_agente_ia(self, request, queryset):
        solicitudes_creadas = revisar_stock_y_generar_solicitudes()
        solicitudes_aprobadas = aprobar_solicitudes_automaticamente()

        mensaje = (
            f" Agente IA ejecutado desde Inventario:\n"
            f"• Solicitudes creadas: {solicitudes_creadas}\n"
            f"• Solicitudes aprobadas: {solicitudes_aprobadas}"
        )
        self.message_user(request, mensaje)
    ejecutar_agente_ia.short_description = "Ejecutar agente IA (revisar stock y aprobar solicitudes)"

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("sku", "name", "price", "reorder_point", "reorder_quantity")

@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ("name", "location")

@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ("product", "warehouse", "change", "movement_type", "created_at")

@admin.register(ProductRequest)
class ProductRequestAdmin(admin.ModelAdmin):
    list_display = ("product", "warehouse", "quantity_requested", "status", "requested_by", "created_at")
    list_filter = ("status", "warehouse")
    search_fields = ("product__name", "requested_by")
    actions = ["ejecutar_agente_ia"]

    def ejecutar_agente_ia(self, request, queryset):
        creadas = revisar_stock_y_generar_solicitudes()
        aprobadas = aprobar_solicitudes_automaticamente()

        mensaje = (
            f" Agente IA ejecutado desde Solicitudes:\n"
            f"• Solicitudes creadas: {creadas}\n"
            f"• Solicitudes aprobadas: {aprobadas}"
        )
        self.message_user(request, mensaje)
    ejecutar_agente_ia.short_description = "Ejecutar agente IA (revisar stock y aprobar solicitudes)"



class CustomAdminSite(admin.AdminSite):
    site_header = "Panel de Inventario con IA"

    def each_context(self, request):
        context = super().each_context(request)
        context["resumen_agente_ia_url"] = reverse("resumen_agente_ia")
        return context

admin_site = CustomAdminSite(name="custom_admin")