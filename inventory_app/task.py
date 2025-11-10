from celery import shared_task
from .models import Inventory, Product
from django.utils import timezone

@shared_task
def check_low_stock_and_notify():
    low = Inventory.objects.filter(quantity__lte=models.F('product__reorder_point')).select_related("product","warehouse")
    results = []
    for inv in low:
        results.append({
            "sku": inv.product.sku,
            "product": inv.product.name,
            "warehouse": inv.warehouse.name,
            "quantity": inv.quantity,
            "reorder_point": inv.product.reorder_point
        })
    # Aquí podrías enviar un correo, webhook o registrar en un log.
    return results