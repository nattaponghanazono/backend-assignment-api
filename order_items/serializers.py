from rest_framework import serializers
from .models import OrderItem
from products.serializers import AllProductSerializer



class OrderitmemsSerializer(serializers.ModelSerializer): 
    class Meta:
        model = OrderItem
        fields = '__all__'

#get
class OrderItemsAllSerializer(serializers.ModelSerializer): 
    product = AllProductSerializer(read_only=True)
    class Meta:
        model = OrderItem
        fields = ['id' ,'quantity', 'price', 'order_id', 'product']



        