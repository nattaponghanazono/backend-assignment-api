
from rest_framework import serializers
from .models import Product, User
from users.serializers import UserSerializer



# post put pathch
class ProductSerializer(serializers.ModelSerializer): # product inner join user with user.id = product.seller_id
    class Meta:
        model = Product
        fields = '__all__'

# get 
class AllProductSerializer(serializers.ModelSerializer):
    seller = UserSerializer(read_only=True)
    class Meta:
        model = Product
        fields = ['id' ,'seller' , 'title' , 'description' , 'image' , 'unit_price']
