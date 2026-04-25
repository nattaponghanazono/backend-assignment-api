from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer , AllProductSerializer


@api_view(['GET'])
def get_products(request):
    products = Product.objects.select_related('seller').all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)



@api_view(['GET'])
def get_products_by_seller(request, pk):
    products = Product.objects.filter(seller_id=pk)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_product_only(request):
    products = Product.objects.all()
    serializer = AllProductSerializer(products, many=True)
    return Response(serializer.data)