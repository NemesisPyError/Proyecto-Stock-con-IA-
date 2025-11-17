#Resumen del agente IA
from django.shortcuts import render
from .models import Product, Inventory, ProductRequest
from django.db import models

# Vista personalizada que muestra un resumen visual del estado del inventario y las solicitudes.
# Se accede desde el panel admin y ayuda a los usuarios a tomar decisiones rápidamente.
def resumen_agente_ia(request):
    total_productos = Product.objects.count()
    stock_bajo = Inventory.objects.filter(quantity__lte=models.F('product__reorder_point')).count()
    solicitudes_total = ProductRequest.objects.count()
    pendientes = ProductRequest.objects.filter(status="PENDING").count()
    aprobadas = ProductRequest.objects.filter(status="APPROVED").count()

    return render(request, "admin/resumen_agente_ia.html", {
        "total_productos": total_productos,
        "stock_bajo": stock_bajo,
        "solicitudes_total": solicitudes_total,
        "pendientes": pendientes,
        "aprobadas": aprobadas,
    })
    
