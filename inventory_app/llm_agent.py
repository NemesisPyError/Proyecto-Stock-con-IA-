from inventory_app.models import Inventory, ProductRequest
from django.db.models import F
from inventory_app.models import ProductRequest, Inventory

# Contiene la lógica del agente IA que revisa el stock, genera solicitudes de reposición y aprueba automáticamente si hay stock suficiente.
# Este archivo permite automatizar decisiones operativas sin intervención humana.
def revisar_stock_y_generar_solicitudes():
    inventarios_bajos = Inventory.objects.filter(quantity__lte=F("product__reorder_point"))
    
    for inv in inventarios_bajos:
        ya_existe = ProductRequest.objects.filter(
            product=inv.product,
            warehouse=inv.warehouse,
            status="PENDING"
        ).exists()

        if not ya_existe:
            ProductRequest.objects.create(
                product=inv.product,
                warehouse=inv.warehouse,
                quantity_requested=inv.product.reorder_quantity,
                requested_by="Agente IA",
                status="PENDING"
            )
            print(f"🧠 Solicitud creada: {inv.product.name} en {inv.warehouse.name}")
        else:
            print(f"🔎 Ya existe solicitud pendiente para {inv.product.name} en {inv.warehouse.name}")



def aprobar_solicitudes_automaticamente():
    solicitudes = ProductRequest.objects.filter(status="PENDING")
    for s in solicitudes:
        try:
            inv = Inventory.objects.get(product=s.product, warehouse=s.warehouse)
            if inv.quantity >= s.quantity_requested:
                s.status = "APPROVED"
                s.save()
                print(f"✅ Solicitud aprobada: {s.product.name} en {s.warehouse.name}")
            else:
                print(f"⛔ No hay stock suficiente para {s.product.name} en {s.warehouse.name}")
        except Inventory.DoesNotExist:
            print(f"❌ No hay inventario para {s.product.name} en {s.warehouse.name}")