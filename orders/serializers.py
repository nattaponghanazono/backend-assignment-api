from rest_framework import serializers
from .models import Order
from users.serializers import UserSerializer
from order_items.serializers import OrderitmemsSerializer
from payments.serializers import PaymentSerializer





class OrderAllSerializer(serializers.ModelSerializer):
    buyer = UserSerializer(read_only=True) 
    items = OrderitmemsSerializer(many=True, read_only=True)
    payment_set = PaymentSerializer(many = True , read_only = True)
    class Meta:
        model = Order
        fields = ['id', 'buyer', 'items', 'total_amount', 'status', 'created_at' , 'payment_set']

# post put pathch
class OrderSerializer(serializers.ModelSerializer): # product inner join user with user.id = product.seller_id
    class Meta:
        model = Order
        fields = '__all__'
