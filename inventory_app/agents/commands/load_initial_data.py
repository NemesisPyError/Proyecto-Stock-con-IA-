from django.core.management.base import BaseCommand
from inventory_app.models import Product, Warehouse, Inventory

class Command(BaseCommand):
    help = "Carga productos, almacenes e inventario inicial"

    def handle(self, *args, **kwargs):
        # Crear productos
        products = [
            {"sku": "SKU001", "name": "Teclado Gamer", "price": 150000, "reorder_point": 10, "reorder_quantity": 30},
            {"sku": "SKU002", "name": "Mouse inalámbrico", "price": 80000, "reorder_point": 15, "reorder_quantity": 40},
            {"sku": "SKU003", "name": "Monitor 24 pulgadas", "price": 899000, "reorder_point": 5, "reorder_quantity": 20},
        ]
        for p in products:
            Product.objects.get_or_create(**p)

        # Crear almacenes
        warehouses = ["Central", "Sucursal San Lorenzo"]
        for name in warehouses:
            Warehouse.objects.get_or_create(name=name, location="Paraguay")

        # Crear inventario inicial
        inventory_data = [
            ("SKU001", "Central", 25),
            ("SKU002", "Central", 10),
            ("SKU003", "Sucursal San Lorenzo", 3),
        ]
        for sku, warehouse_name, qty in inventory_data:
            product = Product.objects.get(sku=sku)
            warehouse = Warehouse.objects.get(name=warehouse_name)
            Inventory.objects.get_or_create(product=product, warehouse=warehouse, defaults={"quantity": qty})

        self.stdout.write(self.style.SUCCESS("✅ Datos iniciales cargados correctamente"))