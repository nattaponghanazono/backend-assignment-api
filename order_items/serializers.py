from rest_framework import serializers
from .models import OrderItem
from orders.models import Order
from products.models import Product
from users.models import User 
from products.serializers import AllProductSerializer



class OrderitmemsSerializer(serializers.ModelSerializer): 
    product = AllProductSerializer(read_only=True)
    class Meta:
        model = OrderItem
        fields = ['id', 'quantity', 'price', 'order_id', 'product' , 'product_id']