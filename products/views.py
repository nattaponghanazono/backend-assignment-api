from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer , AllProductSerializer


@api_view(['GET'])
def get_products(request):
    products = Product.objects.select_related('seller').all()
    serializer = AllProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_product(request, pk):
    try:
        product = Product.objects.select_related('seller').get(pk=pk)
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=404)

    serializer = AllProductSerializer(product, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def create_product(request):
    serializer = ProductSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)

    return Response(serializer.errors, status=400)

@api_view(['PUT', 'PATCH'])
def update_product(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=404)

    serializer = ProductSerializer(product, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
def delete_product(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=404)

    product.delete()
    return Response(status=204)

@api_view(['PUT', 'PATCH'])
def update_stock(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=404)
    
    qty = request.data.get("quantitys")

    if qty is None:
        return Response({"error": "quantitys field is required"}, status=400)

    try:
        qty = int(qty)

        if qty < 0:
            return Response({"error": "quantity must be >= 0"}, status=400)

        product.quantitys += qty   
        product.save()

        return Response({
            "id": product.id,
            "title": product.title,
            "quantitys": product.quantitys,
            "message": "Stock added successfully"
        })

    except (ValueError, TypeError):
        return Response({"error": "quantitys must be a valid integer"}, status=400)