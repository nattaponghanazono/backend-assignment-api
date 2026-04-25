from django.db import models
from orders.models import Order
from products.models import Product

# Create your models here.
class OrderItem(models.Model):
    order = models.ForeignKey(Order , db_column='order_id' , related_name='items' , on_delete= models.CASCADE  )
    product = models.ForeignKey(Product , db_column='product_id' , related_name='order_items' , on_delete=models.CASCADE)
    quantity  = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        db_table  = 'order_items'
    

    def __str__(self):
        return f"Order {self.order.id} - {self.product.title}"

