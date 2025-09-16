from django.db import models
from django.core.validators import MinValueValidator


class Review(models.Model):
    product=models.ForeignKey('Product',on_delete=models.CASCADE,related_name='reviewss')
    name=models.CharField(max_length=255)
    description=models.TextField()
    date=models.DateField(auto_now_add=True)
 

class Promotion(models.Model):
    description=models.CharField(max_length=255)
    discount=models.FloatField()

class Collection(models.Model):
    title=models.CharField(max_length=255)
    #to remove circular dependency
    featured_product=models.ForeignKey(
        'Product',on_delete=models.SET_NULL,null=True,related_name='+') # + tells django to not create reverse realtionship
    
    #changing magic str method to give diff result

    def __str__(self) ->str:
        #return super().__str__() #default implementation
        return self.title
        
class Product(models.Model):
    #sku=models.CharField(max_length=10,primary_key=True)
    title=models.CharField(max_length=255)
    slug=models.SlugField()
    description=models.TextField(null=True,blank=True) #null for DB, blank for admin
    unit_price=models.DecimalField(
        max_digits=6,decimal_places=2,
        validators=[MinValueValidator(1,message='pls select valid value')])
    inventory=models.IntegerField()
    last_update=models.DateTimeField(auto_now=True)
    collection=models.ForeignKey(Collection,on_delete=models.PROTECT,related_name='Productt')
    promotions=models.ManyToManyField(Promotion,related_name='Productz',blank=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering=['title']


class Customer(models.Model):
    MEMBERSHIP_BRONZE='B'
    MEMBERSHIP_SILVER='S'
    MEMBERSHIP_GOLD='G'
    MEMBERSHIP_CHOICES=[
        (MEMBERSHIP_BRONZE,'Bronze'),
        (MEMBERSHIP_SILVER,'Silver'),
        (MEMBERSHIP_GOLD,'Gold')
    ]

    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    email=models.EmailField(unique=True,max_length=255)
    phone=models.CharField(max_length=255)
    birth_date=models.DateField(null=True)
    membership=models.CharField(max_length=1,choices=MEMBERSHIP_CHOICES,default=MEMBERSHIP_BRONZE)

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.phone}"
             
    class Meta:
        
        db_table = 'store_customers'
        indexes = [
            models.Index(fields=['last_name','first_name'])
        ]


class Order(models.Model):
    payment_pending='P'
    payment_complete='C'
    payment_failed='F'
    pay_options=[
        (payment_pending,'PENDING'),
        (payment_complete,'COMPLETE'),
        (payment_failed,'FAILED')
    ]
    payment_status=models.CharField(max_length=1,choices=pay_options,default=payment_pending)
    placed_at=models.DateTimeField(auto_now_add=True)
    customer=models.ForeignKey(Customer,on_delete=models.PROTECT)


class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.PROTECT)
    product=models.ForeignKey(Product,on_delete=models.PROTECT,related_name='orderitems')
    quantity=models.PositiveSmallIntegerField()
    unit_price=models.DecimalField(max_digits=6,decimal_places=2)


class Address(models.Model):
    street=models.CharField(max_length=255)
    city=models.CharField(max_length=255)
    customer=models.OneToOneField(Customer,on_delete=models.CASCADE,primary_key=True)


class Cart(models.Model):
    created_at=models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)  
    quantity=models.PositiveSmallIntegerField()




   


