from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver


# Contiene la definición de los modelos de datos: Product, Warehouse, Inventory, StockMovement y ProductRequest.
# Cada modelo representa una entidad del sistema y define sus relaciones y campos clave.

def revisar_stock_y_generar_solicitudes():
    creadas = 0
    inventarios = Inventory.objects.select_related("product", "warehouse").all()

    for inv in inventarios:
        producto = inv.product
        if inv.quantity <= producto.reorder_point:
            ya_existe = ProductRequest.objects.filter(
                product=producto,
                warehouse=inv.warehouse,
                status="PENDING"
            ).exists()

            if not ya_existe:
                ProductRequest.objects.create(
                    product=producto,
                    warehouse=inv.warehouse,
                    quantity_requested=producto.reorder_quantity,
                    requested_by="Agente IA",
                    status="PENDING"
                )
                creadas += 1

    return creadas


def aprobar_solicitudes_automaticamente():
    aprobadas = 0
    solicitudes = ProductRequest.objects.filter(status="PENDING")

    for solicitud in solicitudes:
        try:
            inventario = Inventory.objects.get(
                product=solicitud.product,
                warehouse=solicitud.warehouse
            )
        except Inventory.DoesNotExist:
            continue

        if inventario.quantity >= solicitud.quantity_requested:
            solicitud.status = "APPROVED"
            solicitud.save()
            aprobadas += 1

    return aprobadas
class Product(models.Model):
    sku = models.CharField("Código SKU", max_length=64, unique=True)
    name = models.CharField("Nombre del producto", max_length=200)
    description = models.TextField("Descripción", blank=True)
    price = models.DecimalField("Precio", max_digits=10, decimal_places=2, default=0.00)
    reorder_point = models.PositiveIntegerField("Punto de reposición", default=10)
    reorder_quantity = models.PositiveIntegerField("Cantidad a reponer", default=50)
    created_at = models.DateTimeField("Creado el", auto_now_add=True)
    updated_at = models.DateTimeField("Actualizado el", auto_now=True)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self):
        return f"{self.sku} - {self.name}"


class Warehouse(models.Model):
    name = models.CharField("Nombre de la sucursal", max_length=150)
    location = models.CharField("Ubicación", max_length=200, blank=True)

    class Meta:
        verbose_name = "Sucursal"
        verbose_name_plural = "Sucursales"

    def __str__(self):
        return self.name


class Inventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="inventories")
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name="inventories")
    quantity = models.IntegerField("Cantidad", default=0)
    last_counted = models.DateTimeField("Último conteo", default=timezone.now)

def save(self, *args, **kwargs):
    super().save(*args, **kwargs)
    # actualizar inventario

    from inventory_app.llm_agent import revisar_stock_y_generar_solicitudes
    revisar_stock_y_generar_solicitudes()
    


    class Meta:
        verbose_name = "Inventario"
        verbose_name_plural = "Inventarios"
        unique_together = ("product", "warehouse")

    def __str__(self):
        return f"{self.product.sku} @ {self.warehouse.name}: {self.quantity}"


class StockMovement(models.Model):
    IN = "IN"
    OUT = "OUT"
    MOVEMENT_CHOICES = [(IN, "Entrada"), (OUT, "Salida")]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="movements")
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name="movements")
    change = models.IntegerField("Cambio de cantidad")
    movement_type = models.CharField("Tipo de movimiento", max_length=3, choices=MOVEMENT_CHOICES)
    created_at = models.DateTimeField("Fecha de movimiento", auto_now_add=True)
    reference = models.CharField("Referencia", max_length=200, blank=True)


def save(self, *args, **kwargs):
    super().save(*args, **kwargs)
    # Actualizar inventario
    inv, _ = Inventory.objects.get_or_create(product=self.product, warehouse=self.warehouse)
    inv.quantity = models.F('quantity') + self.change
    inv.save()
    inv.refresh_from_db()
    inv.last_counted = self.created_at
    inv.save(update_fields=["last_counted", "quantity"])
    
    # Activar agente IA
    revisar_stock_y_generar_solicitudes()

    class Meta:
        verbose_name = "Movimiento"
        verbose_name_plural = "Movimientos"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        inv, _ = Inventory.objects.get_or_create(product=self.product, warehouse=self.warehouse)
        inv.quantity = models.F('quantity') + self.change
        inv.save()
        inv.refresh_from_db()
        inv.last_counted = self.created_at
        inv.save(update_fields=["last_counted", "quantity"])

    def __str__(self):
        return f"{self.get_movement_type_display()} de {self.change} x {self.product.name}"


class ProductRequest(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    quantity_requested = models.PositiveIntegerField("Cantidad solicitada")
    requested_by = models.CharField("Solicitado por", max_length=100)
    status = models.CharField("Estado", max_length=20, choices=[
        ("PENDING", "Pendiente"),
        ("APPROVED", "Aprobado"),
        ("REJECTED", "Rechazado"),
        ("FULFILLED", "Entregado")
    ], default="PENDING")
    created_at = models.DateTimeField("Fecha de solicitud", auto_now_add=True)

    class Meta:
        verbose_name = "Solicitud de producto"
        verbose_name_plural = "Solicitudes de producto"

    def __str__(self):
        return f"Solicitud de {self.quantity_requested} x {self.product.name} ({self.status})"