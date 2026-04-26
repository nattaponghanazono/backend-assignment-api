from django.shortcuts import render

# Create your views here.
# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import OrderItem
from .models import Order
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
    order_id = request.data.get("order")
    items = request.data.get("items")

    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return Response({"error": "Order not found"}, status=404)

    if order.status in ["paid", "shipped"]:
        return Response({"error": "Cannot modify order"}, status=400)

    results = []

    for item in items:
        product = Product.objects.get(id=item['product'])
        quantity = int(item['quantity'])

        if product.quantitys < quantity:
            return Response({
                "error": f"Insufficient stock for {product.title}"
            }, status=400)

        serializer = OrderitmemsSerializer(data={
            "order": order_id,
            "product": product.id,
            "quantity": quantity,
            "price": product.unit_price
        })

        if serializer.is_valid():
            serializer.save()
            results.append(serializer.data)

    return Response(results, status=201)


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