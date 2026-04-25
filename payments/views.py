from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Payment
from .serializers import PaymentAllSerializer , PaymentSerializer


@api_view(['GET'])
def get_payments(request):
    payments = Payment.objects.all()
    serializer = PaymentAllSerializer(payments, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_payment(request, pk):
    try:
        payment = Payment.objects.get(pk=pk)
    except Payment.DoesNotExist:
        return Response({"error": "Payment not found"}, status=404)

    serializer = PaymentAllSerializer(payment, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def create_payment(request):
    serializer = PaymentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)          


@api_view(['PUT', 'PATCH'])
def update_payment(request, pk):
    try:
        payment = Payment.objects.get(pk=pk)
    except Payment.DoesNotExist:
        return Response({"error": "Payment not found"}, status=404)

    serializer = PaymentSerializer(payment, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
def delete_payment(request, pk):
    try:
        payment = Payment.objects.get(pk=pk)
    except Payment.DoesNotExist:
        return Response({"error": "Payment not found"}, status=404)

    payment.delete()
    return Response(status=204)