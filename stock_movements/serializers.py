from rest_framework import serializers
from .models import StockMovement


class StockMovementSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockMovement
        fields = '__all__'

class StockMovementAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockMovement
        fields = ['id', 'product_id', 'change_qty', 'reason', 'created_at']
