from django.contrib import admin

# Register your models here.
from .models import CustomerGroup, Customer, SupplierGroup, Supplier, ProductType, Brand, Product, Order, OrderLine, FeedBack, Message

admin.site.register(CustomerGroup)
admin.site.register(Customer)
admin.site.register(SupplierGroup)
admin.site.register(Supplier)
admin.site.register(ProductType)
admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderLine)
admin.site.register(FeedBack)
admin.site.register(Message)
