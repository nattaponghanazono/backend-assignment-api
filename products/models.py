from django.db import models
from users.models import User


# Create your models here.
class Product(models.Model):
    seller = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column="seller_id",
        related_name="products"
    )
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    image = models.TextField(null=True, blank=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantitys= models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "products"

    def __str__(self):
        return self.title