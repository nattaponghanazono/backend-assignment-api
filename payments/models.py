from django.db import models
from orders.models import Order

# Create your models here


class Payment(models.Model):
    order = models.ForeignKey(Order , related_name='payment' , db_column='order_id' , on_delete=models.CASCADE)
    amount  = models.DecimalField(max_digits=10, decimal_places=2)
    paid_at = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=50)

    class Meta :
        db_table = 'Payment'

    def __str__(self):
        return self.method
    


