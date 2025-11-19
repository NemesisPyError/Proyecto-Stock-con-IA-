# llm_agent.py
from .models import Inventory, ProductRequest
from django.db.models import F

def revisar_stock_y_generar_solicitudes():
    """Crea solicitudes automáticas para productos con stock bajo."""
    creadas = 0
    productos_criticos = Inventory.objects.filter(quantity__lte=F('product__reorder_point'))
    for inv in productos_criticos:
        # Evitar duplicados
        if not ProductRequest.objects.filter(
            product=inv.product,
            warehouse=inv.warehouse,
            status__in=["Pendiente", None]
        ).exists():
            ProductRequest.objects.create(
                product=inv.product,
                warehouse=inv.warehouse,
                quantity_requested=inv.product.reorder_quantity,
                status="Pendiente",
                requested_by="Agente IA"
            )
            creadas += 1
    return creadas

def aprobar_solicitudes_automaticamente():
    """Aprueba automáticamente las solicitudes pendientes si hay stock suficiente."""
    aprobadas = 0
    # Considera Pendiente o null
    solicitudes = ProductRequest.objects.filter(status__in=["Pendiente", None])
    for s in solicitudes:
        inv = Inventory.objects.filter(product=s.product, warehouse=s.warehouse).first()
        if inv and s.quantity_requested <= inv.quantity:
            s.status = "Aprobada"
            s.save()
            # Restar del inventario
            inv.quantity -= s.quantity_requested
            inv.save()
            aprobadas += 1
    return aprobadas
