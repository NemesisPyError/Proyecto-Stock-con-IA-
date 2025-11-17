from django.core.management.base import BaseCommand
from inventory_app.models import Product, Inventory, StockMovement
from django.db.models import Sum
import pandas as pd
import numpy as np

class Command(BaseCommand):
    help = "Agente IA local para sugerir reordenes simples"

    def handle(self, *args, **kwargs):
        recent = StockMovement.objects.filter(movement_type="OUT")
        if not recent.exists():
            self.stdout.write("No hay movimientos salientes registrados.")
            return

        df = pd.DataFrame(list(recent.values("product_id", "change", "created_at")))
        df['date'] = pd.to_datetime(df['created_at']).dt.date
        usage = df.groupby(['product_id', 'date'])['change'].sum().reset_index()

        for prod in Product.objects.all():
            prod_usage = usage[usage.product_id == prod.id]
            if prod_usage.empty:
                avg_daily = 0
            else:
                days = max((prod_usage.date.max() - prod_usage.date.min()).days, 1)
                total = prod_usage.change.sum()
                avg_daily = abs(total) / days

            target_stock = int(np.ceil(avg_daily * 30))
            inv_total = Inventory.objects.filter(product=prod).aggregate(Sum('quantity'))['quantity__sum'] or 0

            if inv_total < target_stock:
                self.stdout.write(
                    f"{prod.sku} - stock actual: {inv_total}, sugerido: {target_stock} (consumo diario: {round(avg_daily,2)})"
                )