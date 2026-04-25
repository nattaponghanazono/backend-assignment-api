from django.db import models
from orders.models import Order

# Create your models here.
class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_at = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=100)

    class Meta :
        db_table = 'payments'
    
    def __str__(self):
        return self.method