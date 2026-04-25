from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import OrderSerializer , OrderAllSerializer
from .models import Order 
from order_items.models import OrderItem 
from django.utils import timezone


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

@api_view(['GET'])
def invoice(request, pk):
    order = Order.objects.get(id=pk)
    items = OrderItem.objects.filter(order=order)

    item_list = []
    total_amount = 0

    for item in items:
        subtotal = float(item.quantity) * float(item.price)
        total_amount += subtotal

        item_list.append({
            "product_title": item.product.title,
            "quantity": item.quantity,
            "unit_price": float(item.price),
            "subtotal": subtotal,
        })

    data = {
        "invoice_no": f"INV-{order.id:04d}",
        "order_id": order.id,
        "created_at": order.created_at,
        "buyer": {
            "username": order.buyer.username,
            "email": order.buyer.email,
            "address": order.buyer.address,
        },
        "items": item_list,
        "total_amount": total_amount,
    }

    return Response(data)





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



@api_view(['PUT'])
def update_payment(request, pk):
    order = Order.objects.get(pk=pk)

    order.paid_amount = request.data.get("paid_amount", 0)
    order.status = "paid"
    order.paid_at = timezone.now()   # ✔ ใช้ได้แล้ว

    order.save()

    return Response({
        "id": order.id,
        "status": order.status,
        "paid_amount": order.paid_amount,
        "paid_at": order.paid_at
    })

@api_view(['DELETE'])
def delete_order(request, pk):
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response({"error": "Order not found"}, status=404)

    order.delete()
    return Response(status=204)

