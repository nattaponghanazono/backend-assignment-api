from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import StockMovement
from .serializers import StockMovementSerializer    
# Create your views here.

@api_view(['GET'])
def get_stock_movements(request):
    stock_movements = StockMovement.objects.all()
    serializer = StockMovementSerializer(stock_movements, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_stock_movement(request, pk):
    try:
        stock_movement = StockMovement.objects.get(pk=pk)
    except StockMovement.DoesNotExist:
        return Response({"error": "Stock movement not found"}, status=404)

    serializer = StockMovementSerializer(stock_movement, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def create_stock_movement(request):
    serializer = StockMovementSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)

    return Response(serializer.errors, status=400)

@api_view(['PUT', 'PATCH'])
def update_stock_movement(request, pk):
    try:
        stock_movement = StockMovement.objects.get(pk=pk)
    except StockMovement.DoesNotExist:
        return Response({"error": "Stock movement not found"}, status=404)

    serializer = StockMovementSerializer(stock_movement, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
def delete_stock_movement(request, pk):
    try:
        stock_movement = StockMovement.objects.get(pk=pk)
    except StockMovement.DoesNotExist:
        return Response({"error": "Stock movement not found"}, status=404)

    stock_movement.delete()
    return Response(status=204)