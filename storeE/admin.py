from django.contrib import admin
from django.db.models.aggregates import Count
from . import models
from django.utils.html import format_html,urlencode
from django.urls import reverse
from django.contrib import messages


class InventoryFilter(admin.SimpleListFilter):
    title='inventory'
    parameter_name='inventory'

    def lookups(self, request, model_admin):
        return [
            ('<10','LOW'),('>10','HIGH')
        ]    
    def queryset(self, request, queryset):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)
        elif self.value() == '>10':
            return queryset.filter(inventory__gt=10)



@admin.register(models.Product) #this class is the admin model for product class   WAY 3
class ProductAdmin(admin.ModelAdmin): #creating this to decide how to view or edit products in admin
    #customing forms
    #fields=['title','slug']
    #exclude=['promotions']
    #readonly_fields=['title']
    autocomplete_fields=['collection']
    prepopulated_fields={
        'slug':['title']
    }

    actions=['clear_inventory']
    list_display=['title','unit_price','inventory_status','collection_title']
    list_editable=['unit_price']
    list_per_page=15
    list_select_related=['collection']
    list_filter=['collection','last_update',InventoryFilter]
    search_fields=['title']

    def collection_title(self,product):
        return product.collection.title

    @admin.display(ordering='inventory')
    def inventory_status(self,Product):
        return 'OK'if Product.inventory>20 else 'LOW'
    
    @admin.action(description='Clear Inventory')
    def clear_inventory(self,request,queryset):
        updated_count=queryset.update(inventory=0)
        self.message_user(
            request,
            f'{updated_count} products were successfully updated',
            messages.ERROR#from messages class
        )
            
#admin.site.register(models.Product)#way1 to register
#admin.site.register(models.Product,ProductAdmin) # way 2 to register

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display=['first_name','last_name','membership','no_of_orders']
    list_editable=['membership']
    ordering=['first_name','last_name']
    list_per_page=20
    search_fields=['first_name__istartswith','last_name__istartswith']

    #view orders of each customer
    '''
    @admin.display(ordering='no_of_orders')
    def no_of_orders(self,customer):
        return customer.no_of_orders
    '''
    @admin.display(ordering='no_of_orders')
    def no_of_orders(self,customer):
        url=(reverse('admin:storeE_order_changelist')
        +'?'
        +urlencode({
            'customer__id':str(customer.id)
        }))
        return format_html('<a href="{}">{} Orders</a>',url,customer.no_of_orders)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            no_of_orders=Count('order')
        )

class OrderItemInline(admin.TabularInline): #admin.StackedInline
    autocomplete_fields=['product']
    min_num=1
    max_num=10
    model=models.OrderItem
    extra=0

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields=['customer']
    inlines=[OrderItemInline]
    list_display=['id','placed_at','customer']#'customer_name']  
    #list_select_related=['customer']
    #ordering=['placed_at']

    #def customer_name(self,order):
     #   return order.customer.first_name
@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display=['title','products_count']

    search_fields=['title'] #auto-complete in products
    #Annotation
    '''
    def products_count(self,collection):
    @admin.display(ordering='products_count')
        return collection.products_count '''
    
    #link
    @admin.display(ordering='products_count')
    def products_count(self,collection):
        url=(reverse('admin:storeE_product_changelist')#admin:app_model_page
             +'?'
             +urlencode({ #query string
                 'collection__id':str(collection.id)
             }))
        return format_html('<a href="{}">{}</a>',url,collection.products_count)

    
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count=Count('productt')
        )
    


#admin.site.register(models.Collection)




# Register your models here.
