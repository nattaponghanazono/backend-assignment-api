from rest_framework import serializers
from users.models import User
from products.models import Product
from  order_items.models import OrderItem
from .models import Order


class UserSerializer(serializers.ModelSerializer): #user 
    class Meta:
        model = User
        fields = ['username', 'email', 'address']

class AllProductSerializer(serializers.ModelSerializer): #product  join users 
    seller = UserSerializer(read_only = True)
    class Meta:
        model = Product
        fields = ['id' , 'title' , 'unit_price' , 'quantitys'  ,'seller']

class OrderitmemsSerializer(serializers.ModelSerializer): #order_itmes inner joing product
    product = AllProductSerializer(read_only=True)
    class Meta:
        model = OrderItem
        fields = ['id', 'quantity', 'price', 'order_id', 'product']


class OrderSerializer(serializers.ModelSerializer): #user inner join (order_itmes inner joing product)
    buyer = UserSerializer(read_only=True) 
    items = OrderitmemsSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = ['id', 'buyer', 'items', 'total_amount', 'status', 'created_at']