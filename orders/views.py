from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import OrderSerializer
from .models import Order

# Create your views here. OrderSerializers
@api_view(['GET'])
def get_data(request):
    order = Order.objects.select_related('buyer').all()
    serializers = OrderSerializer(order , many = True)
    return Response(serializers.data)



@api_view(['GET'])
def get_orders(request):
    orders = Order.objects.select_related('buyer').prefetch_related('items').prefetch_related('payment')
    print(orders.query)
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)

