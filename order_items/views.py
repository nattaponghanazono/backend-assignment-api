from django.shortcuts import render

# Create your views here.
# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import OrderItem
from .serializers import OrderItemsAllSerializer , OrderitmemsSerializer
from products.models import Product



@api_view(['GET'])
def get_order_items(request):
    order_items = OrderItem.objects.all()
    serializer = OrderItemsAllSerializer(order_items, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_order_item(request, pk):
    try:
        order_item = OrderItem.objects.get(pk=pk)
    except OrderItem.DoesNotExist:
        return Response({"error": "Order item not found"}, status=404)

    serializer = OrderItemsAllSerializer(order_item, many=False)
    return Response(serializer.data)



@api_view(['POST'])
def create_order_item(request):
    data = request.data.copy()

    product = Product.objects.get(id=data['product'])
    
    # 🔥 backend set price เอง (สำคัญ)
    data['price'] = product.unit_price

    serializer = OrderitmemsSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)

    return Response(serializer.errors, status=400)


@api_view(['PUT', 'PATCH'])
def update_order_item(request, pk):      
    try:
        order_item = OrderItem.objects.get(pk=pk)
    except OrderItem.DoesNotExist:
        return Response({"error": "Order item not found"}, status=404)

    serializer = OrderitmemsSerializer(order_item, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=400)      

@api_view(['DELETE'])
def delete_order_item(request, pk):     
    try:
        order_item = OrderItem.objects.get(pk=pk)
    except OrderItem.DoesNotExist:
        return Response({"error": "Order item not found"}, status=404)

    order_item.delete()
    return Response(status=204)