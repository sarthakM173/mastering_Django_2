from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Product
from .serializer import ProductSerializer

from rest_framework import status

#def product_list(request):   
#    return HttpResponse('ok')

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

@api_view()
def collection_details(request,pk):
      return Response("OK")        
                                    