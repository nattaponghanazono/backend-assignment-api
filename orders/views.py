from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import OrderSerializer , OrderAllSerializer
from .models import Order

# Create your views here. OrderSerializers
@api_view(['GET'])
def get_data(request):
    order = Order.objects.select_related('buyer').all()
    serializers = OrderAllSerializer(order , many = True)
    return Response(serializers.data)

@api_view(['GET'])
def get_orders(request, pk):
    try:
        order = Order.objects.select_related('buyer').prefetch_related('items').prefetch_related('payment').get(pk=pk)
    except Order.DoesNotExist:
        return Response({"error": "Order not found"}, status=404)

    print(order.query)
    serializer = OrderAllSerializer(order, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def create_order(request):
    serializer = OrderSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)

    return Response(serializer.errors, status=400)  

@api_view(['PUT', 'PATCH'])
def update_order(request, pk):          
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response({"error": "Order not found"}, status=404)

    serializer = OrderSerializer(order, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=400)


@api_view(['DELETE'])
def delete_order(request, pk):
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response({"error": "Order not found"}, status=404)

    order.delete()
    return Response(status=204)

