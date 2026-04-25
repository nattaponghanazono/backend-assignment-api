from rest_framework import serializers
from .models import Order
from users.serializers import UserSerializer
from order_items.serializers import OrderItemsAllSerializer






class OrderAllSerializer(serializers.ModelSerializer):
    buyer = UserSerializer(read_only=True) 
    items = OrderItemsAllSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = ['id', 'buyer', 'items', 'status', 'created_at' ]

# post put pathch
class OrderSerializer(serializers.ModelSerializer): # product inner join user with user.id = product.seller_id
    class Meta:
        model = Order
        fields = '__all__'
