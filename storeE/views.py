from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Product,Collection,OrderItem,Review,Cart,CartItem
from .serializer import ProductSerializer,CollectionSerializer,ReviewSerializer,CartSerializer,CartItemSerializer

from rest_framework import status

from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.mixins import ListModelMixin,CreateModelMixin
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ProductFilter
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.pagination import PageNumberPagination
from .pagination import DefaultPagination



class CartViewSet(CreateModelMixin,GenericViewSet):
     queryset=Cart.objects.all()
     serializer_class=CartSerializer
     filter_backends=[]


class CartItemSet(ModelViewSet):
     queryset=CartItem.objects.all()
     serializer_class=CartItemSerializer




class ProductViewSet(ModelViewSet): #ReadOnlyModelViewSet--to only list no update create delete
     queryset=Product.objects.all()#we dont need select_related
     serializer_class=ProductSerializer
     filter_backends=[DjangoFilterBackend,SearchFilter,OrderingFilter]
     filterset_class=ProductFilter
     pagination_class=DefaultPagination
     search_fields=['title','description']
     ordering_fields=['unit_price','last_update']
    


     '''#filter    
     def get_queryset(self):
          queryset=Product.objects.all()
          collection_id=self.request.query_params['collection_id']
          if collection_id:
               queryset=queryset.filter(collection_id=collection_id)
          return queryset'''

     def get_serializer_context(self):
            return {'request':self.request}
     
     def destroy(self, request,*args,**kwargs):
            if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
                return Response({'error':'Product cannot be deleted because it is associated to an order item'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
            return super().destroy(request,*args,**kwargs)
         
class ReviewViewSet(ModelViewSet):
     queryset=Review.objects.all()
     serializer_class=ReviewSerializer


     def get_queryset(self):
          return Review.objects.filter(product_id=self.kwargs['product_pk'])

     def get_serializer_context(self):
          return {'product_id':self.kwargs['product_pk']}
     

class CollectionViewSet(ModelViewSet):
     queryset=Collection.objects.annotate(total_products=Count('Productt')).all()
     serializer_class=CollectionSerializer

     def destroy(self, request,*args,**kwargs):
            if Product.collection.filter(product_id=kwargs['pk']).count() > 0:
                return Response({'error':'Collection cannot be deleted bcz it is associated to product(s)'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
            return super().destroy(request,*args,**kwargs)


class ProductList(ListCreateAPIView):
        queryset=Product.objects.select_related('collection').all()
        serializer_class=ProductSerializer

       #def get(self, request, *args, **kwargs):
        #    return Product.objects.select_related('collection').all()
        def get_serializer_context(self):
             return {'request':self.request}
        
class ProductDetials(RetrieveUpdateDestroyAPIView):
     queryset=Product.objects.all()
     serializer_class= ProductSerializer
     lookup_field='id'

     def delete(self,request,id):
        product=get_object_or_404(Product,pk=id)
        if product.orderitems.count()>0:
                return Response({'error':'Product cannot be deleted because it is associated to an order item'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

        
class CollectionList(ListCreateAPIView):
     queryset=Collection.objects.annotate(total_products=Count('Productt')).all()
     serializer_class=CollectionSerializer


class CollectionDetails(RetrieveUpdateDestroyAPIView):
     queryset=Collection.objects.annotate(total_product=Count('Productt'))
     serializer_class=CollectionSerializer

     def delete(self,request,pk):
        collection=get_object_or_404(Collection,pk=pk)
        if collection.Productt.count():
            return Response({'error':'Collection cannot be deleted bcz it is associated to product(s)'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#CLASS Based View
'''
class ProductList(APIView):
    def get(self,request):
        queryset=Product.objects.select_related('collection').all()
        serializer=ProductSerializer(queryset,many=True,context={'request':request})
        return Response(serializer.data)
    def post(self,request):
          serializer=ProductSerializer(data=request.data)
          serializer.is_valid(raise_exception=True)
          serializer.save()
          return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class ProductDetails(APIView):  
    def get(self,request,id):
        product=get_object_or_404(Product,pk=id)
        serializer=ProductSerializer(product)
        return Response(serializer.data)
    
    def put(self,request,id):
        product=get_object_or_404(Product,pk=id)
        serializer=ProductSerializer(product,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def delete(self,request,id):
        product=get_object_or_404(Product,pk=id)
        if product.orderitems.count()>0:
                return Response({'error':'Product cannot be deleted because it is associated to an order item'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    '''






#all below are function based view
'''
@api_view(['GET','POST'])
def product_list(request):
    if request.method == 'GET':
        queryset=Product.objects.select_related('collection').all()
        #serializer=ProductSerializer(queryset,many=True)
        serializer=ProductSerializer(queryset,many=True,context={'request':request})
        return Response(serializer.data)
    elif request.method == 'POST':
          serializer=ProductSerializer(data=request.data)
          serializer.is_valid(raise_exception=True)
          serializer.save()
          #print(serializer.validated_data)
          return Response(serializer.data, status=status.HTTP_201_CREATED)
          
'''

@api_view()
def product_details(request,id):
    #try: #way 1    
        #product=Product.objects.get(pk=id)
        product=get_object_or_404(Product,pk=id)#404 way2
        serializer=ProductSerializer(product) #will convert Product obj into dict 
        return Response(serializer.data)# somewhere under the hood django will give this dict to render which will 
                                            #convert it into json and put it in serializer.data
    #except Product.DoesNotExist:
        #return Response(status=404)
        #return Response(status=status.HTTP_404_NOT_FOUND)
'''

@api_view(['GET','PUT','DELETE'])
def product_details(request,id):
    product=get_object_or_404(Product,pk=id)
    if request.method == 'GET':
        serializer=ProductSerializer(product)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer=ProductSerializer(product,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK) #its convention to return the data we created 
    elif request.method == 'DELETE':
        if product.orderitems.count()>0:
                return Response({'error':'Product cannot be deleted because it is associated to an order item'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

@api_view(['GET','POST'])    
def collection_list(request):
    if request.method =='GET':
        queryset=Collection.objects.annotate(total_products=Count('Productt')).all()
        serializer=CollectionSerializer(queryset,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    elif request.method == 'POST': 
        serializer=CollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
'''
         


@api_view(['GET','PUT','DELETE'])
def collection_details(request,id):
    collection=get_object_or_404(
            Collection.objects.annotate(
            total_products=Count('Productt')),pk=id)
    if request.method=='GET':
        serializer=CollectionSerializer(collection)
        return Response(serializer.data,status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer=CollectionSerializer(collection,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
    elif request.method == 'DELETE':
        if collection.Productt.count():
            return Response({'error':'Collection cannot be deleted bcz it is associated to product(s)'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
         
    return Response("OK")
        
                                    