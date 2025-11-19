from django.contrib import admin, messages
from django.db.models import F
from django.urls import reverse
from django.shortcuts import render
from .models import Product, Warehouse, Inventory, StockMovement, ProductRequest
from .llm_agent import revisar_stock_y_generar_solicitudes, aprobar_solicitudes_automaticamente
from .agente_ia import ejecutar_agente_ia_inteligente
from django.utils.html import format_html


# Configuración del panel de administración
admin.site.site_header = "Autoservice Los Hermanos"
admin.site.site_title = "Autoservice Los Hermanos"
admin.site.index_title = "Panel de Administración"


# Acción global: Ejecutar Agente IA
@admin.action(description="Ejecutar Agente IA sobre inventario")
def ejecutar_agente_ia(self, request, queryset):
    creadas, aprobadas = ejecutar_agente_ia_inteligente()
    self.message_user(
        request,
        f"🤖 Agente IA ejecutado:\n• Solicitudes creadas: {creadas}\n• Solicitudes aprobadas: {aprobadas}"
    )


# InventoryAdmin
@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ("product", "warehouse", "quantity", "last_counted", "stock_status")
    list_filter = ("warehouse",)
    search_fields = ("product__name", "warehouse__name")
    actions = ["ejecutar_agente_ia"]

    def stock_status(self, obj):
        return "Bajo" if obj.quantity <= obj.product.reorder_point else "OK"
    stock_status.short_description = "Estado de stock"

    @admin.action(description="Ejecutar Agente IA (revisar stock y aprobar solicitudes)")
    def ejecutar_agente_ia(self, request, queryset):
        creadas = revisar_stock_y_generar_solicitudes()
        aprobadas = aprobar_solicitudes_automaticamente()
        self.message_user(
            request,
            f"🤖 Agente IA ejecutado desde Inventario:\n"
            f"• Solicitudes creadas: {creadas}\n"
            f"• Solicitudes aprobadas: {aprobadas}"
        )


# ProductAdmin
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("sku", "name", "price", "reorder_point", "reorder_quantity")
    search_fields = ("name", "sku")


# WarehouseAdmin
@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ("name", "location")
    search_fields = ("name",)


# StockMovementAdmin
@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ("product", "warehouse", "change", "movement_type", "created_at")
    list_filter = ("movement_type", "warehouse")
    search_fields = ("product__name",)


# ProductRequestAdmin
@admin.register(ProductRequest)
class ProductRequestAdmin(admin.ModelAdmin):
    list_display = ("product", "warehouse", "quantity_requested", "status",
                    "requested_by", "created_at")
    list_filter = ("status", "warehouse")
    search_fields = ("product__name", "requested_by")
    actions = ["ejecutar_agente_ia"]

    @admin.action(description="Ejecutar Agente IA (revisar stock y aprobar solicitudes)")
    def ejecutar_agente_ia(self, request, queryset):
        creadas = revisar_stock_y_generar_solicitudes()
        aprobadas = aprobar_solicitudes_automaticamente()
        self.message_user(
            request,
            f"🤖 Agente IA ejecutado desde Solicitudes:\n"
            f"• Solicitudes creadas: {creadas}\n"
            f"• Solicitudes aprobadas: {aprobadas}"
        )


# Vista personalizada Resumen Agente IA
def resumen_agente_ia(request):
    creadas = revisar_stock_y_generar_solicitudes()
    aprobadas = aprobar_solicitudes_automaticamente()
    datos = {"creadas": creadas, "aprobadas": aprobadas}
    return render(request, "admin/resumen_agente_ia.html", {"datos": datos})


# AdminSite personalizado
class CustomAdminSite(admin.AdminSite):
    site_header = "Panel de Inventario con IA"

    def each_context(self, request):
        context = super().each_context(request)
        context["resumen_agente_ia_url"] = reverse("resumen_agente_ia")
        return context


admin_site = CustomAdminSite(name="custom_admin")
