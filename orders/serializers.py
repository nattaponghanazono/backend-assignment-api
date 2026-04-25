from rest_framework import serializers
from users.models import User
from products.models import Product
from  order_items.models import OrderItem
from .models import Order
from users.serializers import UserSerializer
from order_items.serializers import OrderitmemsSerializer
from payments.serializers import PaymentSerializer





class OrderSerializer(serializers.ModelSerializer):
    buyer = UserSerializer(read_only=True) 
    items = OrderitmemsSerializer(many=True, read_only=True)
    payment = PaymentSerializer(many = True , read_only = True)
    class Meta:
        model = Order
        fields = ['id', 'buyer', 'items', 'total_amount', 'status', 'created_at' , 'payment']

