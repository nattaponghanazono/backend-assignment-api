
from rest_framework import serializers
from .models import Product, User

#UserSerializer
class UserSerializer(serializers.ModelSerializer): 
    class Meta:
        model = User
        fields = ['id', 'username', 'email']



class ProductSerializer(serializers.ModelSerializer): # product inner join user with user.id = product.seller_id
    seller = UserSerializer(read_only=True)
    class Meta:
        model = Product
        fields = ['seller' , 'title' , 'description' , 'image' , 'unit_price']


class AllProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'