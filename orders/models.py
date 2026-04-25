from django.db import models
from users.models import User

# Create your models here.
class Order(models.Model):
    buyer = models.ForeignKey(User , db_column="buyer_id" , related_name="orders" , on_delete = models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=50, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        db_table = "orders"

    def __str__(self):
        return self.status
