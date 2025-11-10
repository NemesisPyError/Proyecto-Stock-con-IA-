from django.db import models
from django.utils import timezone

class Product(models.Model):
    sku = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    reorder_point = models.PositiveIntegerField(default=10)
    reorder_quantity = models.PositiveIntegerField(default=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.sku} - {self.name}"

class Warehouse(models.Model):
    name = models.CharField(max_length=150)
    location = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name

class Inventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="inventories")
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name="inventories")
    quantity = models.IntegerField(default=0)
    last_counted = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ("product", "warehouse")

    def __str__(self):
        return f"{self.product.sku} @ {self.warehouse.name}: {self.quantity}"

class StockMovement(models.Model):
    IN = "IN"
    OUT = "OUT"
    MOVEMENT_CHOICES = [(IN, "IN"), (OUT, "OUT")]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="movements")
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name="movements")
    change = models.IntegerField()
    movement_type = models.CharField(max_length=3, choices=MOVEMENT_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    reference = models.CharField(max_length=200, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        inv, _ = Inventory.objects.get_or_create(product=self.product, warehouse=self.warehouse)
        inv.quantity = models.F('quantity') + self.change
        inv.save()
        inv.refresh_from_db()
        inv.last_counted = self.created_at
        inv.save(update_fields=["last_counted", "quantity"])
    
class ProductRequest(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    quantity_requested = models.PositiveIntegerField()
    requested_by = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=[
        ("PENDING", "Pendiente"),
        ("APPROVED", "Aprobado"),
        ("REJECTED", "Rechazado"),
        ("FULFILLED", "Entregado")
    ], default="PENDING")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Solicitud de {self.quantity_requested} x {self.product.name} ({self.status})"