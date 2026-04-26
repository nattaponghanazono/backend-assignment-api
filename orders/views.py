import uuid


from collections import defaultdict
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import OrderSerializer , OrderAllSerializer
from .models import Order 
from order_items.models import OrderItem 
from django.utils import timezone
from django.shortcuts import get_object_or_404
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



@api_view(['DELETE'])
def delete_order(request, pk):
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response({"error": "Order not found"}, status=404)

    order.delete()
    return Response(status=204)


@api_view(['GET'])
def shipping_label(request, pk):
    try:
        order = Order.objects.select_related('buyer').get(pk=pk)
    except Order.DoesNotExist:
        return Response({"error": "Order not found"}, status=404)

    items = OrderItem.objects.filter(order=order).select_related('product')

    if not items.exists():
        return Response({"error": "Order has no items"}, status=400)

    item_list = []
    total_amount = 0

    for item in items:
        subtotal = float(item.quantity) * float(item.price)
        total_amount += subtotal

        item_list.append({
            "product_id": item.product.id,
            "product_title": item.product.title,
            "quantity": item.quantity,
            "unit_price": float(item.price),
            "subtotal": subtotal,
        })

    data = {
        "shipping_label_no": f"SHP-{order.id:04d}",
        "order_id": order.id,
        "created_at": order.created_at,

        "buyer": {
            "username": order.buyer.username,
            "email": order.buyer.email,
            "address": order.buyer.address,
        },

        "items": item_list,
        "total_items": sum(item["quantity"] for item in item_list),
        "total_amount": total_amount,
        "status": order.status,
    }

    return Response(data)




from collections import defaultdict
from django.db import transaction

@api_view(['PUT'])
def ship_order(request, pk):

    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response({"error": "Order not found"}, status=404)

    items = OrderItem.objects.select_related('product').filter(order=order)

    if order.status == "shipped":
        return Response({
            "message": "Already shipped",
            "tracking_number": f"TH-{order.id:04d}"
        })

    # 🔥 GROUP PRODUCT FIRST
    product_map = defaultdict(int)

    for item in items:
        product_map[item.product] += item.quantity

    with transaction.atomic():

        # ✔ check stock first
        for product, qty in product_map.items():
            if product.quantitys < qty:
                return Response({
                    "error": f"Insufficient stock for {product.title}",
                    "available": product.quantitys,
                    "required": qty
                }, status=400)

        # ✔ deduct stock once per product
        for product, qty in product_map.items():
            product.quantitys -= qty
            product.save()

        order.status = "shipped"
        order.save()

    return Response({
        "message": "Order shipped successfully",
        "order_id": order.id,
        "tracking_number": f"TH-{order.id:04d}",
        "status": order.status
    })


@api_view(['PUT'])
def update_payment(request, pk):
    order = get_object_or_404(Order, pk=pk)

    # ❗ กันจ่ายซ้ำ
    if order.status == "paid":
        return Response({
            "message": "Order already paid",
            "order_id": order.id,
            "status": order.status
        })

    # ❗ กันจ่ายหลังส่งของ
    if order.status == "shipped":
        return Response({
            "error": "Order already shipped, cannot pay"
        }, status=400)

    # เปลี่ยนสถานะเป็น paid
    order.status = "paid"

    # optional: บันทึก payment method ถ้ามี field
    payment_method = request.data.get("method")
    if payment_method:
        order.payment_method = payment_method

    order.save()

    return Response({
        "message": "Payment confirmed",
        "order_id": order.id,
        "status": order.status
    })