from rest_framework import serializers
from .models import OrderItem
from orders.models import Order
from products.models import Product
from users.models import User 
from products.serializers import ProductSerializer



class OrderitmemsSerializer(serializers.ModelSerializer): 
    class Meta:
        model = OrderItem
        fields = '__all__'

#get
class OrderItemsAllSerializer(serializers.ModelSerializer): 
    product = ProductSerializer(read_only=True)
    class Meta:
        model = OrderItem
        fields = ['quantity', 'price', 'order_id', 'product' ]



        