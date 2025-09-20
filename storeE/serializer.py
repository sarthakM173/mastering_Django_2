from rest_framework import serializers
from .models import Product,Collection,Review,Cart,CartItem
from decimal import Decimal


class CartSerializer(serializers.ModelSerializer):
     id=serializers.UUIDField(read_only=True)
     class Meta:
          model=Cart
          fields=['id']


class CartItemSerializer(serializers.ModelSerializer):
     class Meta:
          model=CartItem
          fields=['product','quantity']














class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
          model=Review
          fields=['id','name','description','date']

    def create(self,validated_data):
          product_id=self.context['product_id']
          return Review.objects.create(product_id=product_id,**validated_data)

class CollectionSerializer(serializers.ModelSerializer):
    total_products=serializers.IntegerField(read_only=True)  
    #total_products=serializers.SerializerMethodField(method_name='getC')
    class Meta:
        model=Collection
        fields=['id','title','total_products','featured_product']

    #def getC(self,collection:Collection):
     #    return collection.Productt.count()
    
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model= Product
        fields=['id','description','slug','title','unit_price','inventory','price_with_tax','collection']

    price_with_tax=serializers.SerializerMethodField(method_name='cal_tax')

    def cal_tax(self,product: Product):
            return product.unit_price * Decimal(1.1)
    ''' #overriding create and update
    def create(self, validated_data):   #change the creation process in database
         product=Product(**validated_data) #umpacking the dictionary
         product.other = 1
         product.save()
         return product
    def update(self,instance,validated_data): #instance is a product object
         instance.unit_price=validated_data.get('unit_price')
         instance.save()
         return instance
    '''     
         
        
        
    
"""
class ProductSerializer(serializers.Serializer):
    id= serializers.IntegerField()
    title=serializers.CharField(max_length=255)
    price=serializers.DecimalField(max_digits=6,decimal_places=2,source='unit_price')
    price_with_tax=serializers.SerializerMethodField(method_name='cal_tax')
    '''#way 1 custom related fields
    collection=serializers.PrimaryKeyRelatedField(
        queryset=Collection.objects.all()
    )'''
    #way2
    #collection=serializers.StringRelatedField()
    #way3
    #collection=CollectionSerializes()
    #way4
    collection=serializers.HyperlinkedRelatedField(
        queryset=Collection.objects.all(),
        view_name='collection-detail'
    )
    """
