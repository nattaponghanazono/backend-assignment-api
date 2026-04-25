from django.db import models

# Create your models here.
class StockMovement(models.Model):
    product_id = models.IntegerField()
    change_qty = models.IntegerField()
    reason = models.CharField(max_length=10)  # 'in' or 'out'
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'stock_movements'

    def __str__(self):
        return f"{self.reason} - Product ID: {self.product_id} - Quantity: {self.change_qty}"