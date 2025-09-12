from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from tags.models import TaggedItem
from storeE.models import Product
from storeE.admin import ProductAdmin


class TagInline(GenericTabularInline):
    autocomplete_fields=['tag']
    model=TaggedItem


class CustomProductAdmin(ProductAdmin):    
    inlines=[TagInline]


admin.site.unregister(Product)
admin.site.register(Product,CustomProductAdmin)


# Register your models here.
