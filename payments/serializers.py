
from rest_framework import serializers
from .models import Payment
from orders.serializers import OrderitmemsSerializer

class PaymentSerializer(serializers.ModelSerializer):  
    class Meta:
        fields = ['id' , 'order_id' , 'amount' , 'paid_at' , 'method']