from django.shortcuts import render
from storeE.models import Product,OrderItem,Order,Customer,Collection
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q,F,Avg,Value,Func,ExpressionWrapper,DecimalField
from django.db.models.functions import Concat
from django.db.models.aggregates import Count,Max,Min,Avg,Sum
#from decimal import Decimal
from django.contrib.contenttypes.models import ContentType
from tags.models import TaggedItem
from django.db import transaction
from django.db import connection



def say_hello(request):
#pull data from Database
# tranform data
# send email   
   # return HttpResponse('Hello World')

   #queryset
   #query_set=Product.objects.all() #this returns a queryset and standalone it won't elauate query
   ##query_set.filter().filter().orderby()
   #for product in query_set:
      #print(product)
   #object
   #product=Product.objects.get(pk=1) #here we get single object so not a queryset and the query will be evaluted 

   '''Using try and catch block   
   try:
      product=Product.objects.get(pk=0)   
   except ObjectDoesNotExist:
      pass  ''' 
   
   #None 
   #product=Product.objects.filter(pk=0).first()

   #Boolean
   #exists=Product.objects.filter(pk=0).exists()

   #using lookups 
   #query_set=Product.objects.filter(unit_price__range=(20,30))
   #query_set=Product.objects.filter(collection__id__range=(1,20))

   #more filtering
   #query_set=Product.objects.filter(last_update__year=2021)
   #query_set=query_set.filter(title__contains="coffee")

   '''where avg unit_price<unit_price
   from decimal import Decimal, ROUND_HALF_UP
   av=Product.objects.aggregate(Avg('unit_price'))
   query_set=Product.objects.filter(unit_price__gt=av['unit_price__avg'].quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))'''
   

   #using lookups with str
   #query_set=Product.objects.filter(title__contains='coffee') #icontains- to make itcase sensitive, __starswith,__endswith 

   #OR
   #query_set=Product.objects.filter(Q(inventory__lt=10) | Q(unit_price__lte=20))

   #F
   #query_set=Product.objects.filter(inventory__lt=F('unit_price'))

   #sorted data
   #product=Product.objects.order_by('-title','unit_price').reverse()[0]
   #product=Product.objects.earliest('unit_price') #sort data on unit proce gives topmost element
   #product=Product.objects.latest('title') #sort data desc and give top

   #limit
   #query_set=Product.objects.all()[5:10]

   #inner-join
   #query_set=Product.objects.values('id','title','collection__title')#we get dictionaries insted of objects
   #query_set=Product.objects.values_list('id','title','collection__title')#we get tuples

   #products ordered and sort by title
   ##query_set=OrderItem.objects.values('product_id').distinct()#product_id is not a field but will be created during runtime bcz foreignkey 
   #query_set=Product.objects.filter(id__in=OrderItem.objects.values('product_id').distinct()).sort_by('title')

   #only,defer

   #select_related-Join (for one object)
   #queryset=Product.objects.select_related('collection').all() #(collection__someOtherRelatedField) to collection
   #prefetch_related-Join (for many object)
   #queryset=Product.objects.prefetch_related('promotions').select_related('collection').all()

   #get last 5 order with their customer and items
   #queryset=Order.objects.select_related('customer').prefetch_related('orderitem_set__product').order_by('-placed_at')[:5]
   #return render(request,'hello.html',{'name':'Humans','orders':queryset})


   #Aggregations - as it one of the methods of queryset we can use it with other methods
   #result=Product.objects.filter(collection__id=1).aggregate(Count('id'),min_val=Min('unit_price'))#returns a dict

   #annotate
   #queryset=Product.objects.annotate(is_new=Value(True))
   #queryset=Product.objects.annotate(new_id=F('id')+1)
   #calling db func way 1
   '''
   queryset=Customer.objects.annotate(
      full_name=Func(F('first_name'),Value(' '),
                     F('last_name'),function='CONCAT')
   )'''
   #Way 2
   '''
   queryset=Customer.objects.annotate(
      full_name=Concat('first_name',Value(' '),'last_name')
   )'''
   
   #group_by
   #queryset=Customer.objects.annotate(orders_count=Count('order'))

   #expressionWrapper
   #discounted_price=ExpressionWrapper( F('unit_price') * 0.8,output_field=DecimalField(max_digits=10,decimal_places=2))
   #queryset=Product.objects.annotate(discounted_price=discounted_price)      

   #Generic relationship
   '''
   content_type_id=ContentType.objects.get_for_model(Product)
   queryset=TaggedItem\
      .objects.select_related('tag')\
      .filter(
         content_type=content_type_id,
         object_id=1)'''
   ##customer manager
   #queryset=TaggedItem.objects.get_tags_for(Product,1)

   #raw query
   #queryset=Product.objects.raw('SELECT id,title FROM sroreE_collection')
   ##without using model mapper
   '''
   with connection.cursor() as cursor:
      cursor.execute('SELECT* FROM')
      cursor.callproc('')#for storage procedure
      '''
  
   
   #return render(request,'hello.html',{'name':'Humans','products': list(queryset)})

   #===================================================DDL query
   #way1 INSERT
   '''
   collection=Collection()
   collection.title='Video Games'
   collection.featured_product=Product(pk=1)#pk1 should exist
   collection.save()'''
   #way2
   #collection=Collection.objects.create(title='a',featured_product=1)#if names of the fields(title,fea..) are changed it wont update dynamically
   #collection.id

   #update
   #collection=Collection(pk=11)#will make other column vals empty
   #collection=Collection.objects.get(pk=11)#this will call the oject to memory then update it which is bit more expensive
   #collection.featured_product=None
   #collection.save()

   #Collection.objects.filter(pk=11).update(featured_product=None)#faster but not dynamic

   #DELETE
   #collection=Collection(pk=11)
   #collection.delete()

   #Collection.objects.filter(id__gt=11).delete()
   '''
   with transaction.atomic():
      order=Order()
      order.customer_id=1
      order.save()

      item=OrderItem()
      item.order=order
      item.product_id=1
      item.quantity=1
      item.unit_price=10
      item.save()'''

   return render(request,'hello.html',{'name':'Humans'})
   