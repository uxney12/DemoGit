# Create your models here.
from django.db import models
from django.urls import reverse  
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower
from django.conf import settings
from datetime import date

class CustomerGroup(models.Model):
    group_code = models.CharField(max_length=255)
    group_name = models.CharField(max_length=255, null=True, blank=True)
    group_type = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=10000, null=True, blank=True)
    customer_count = models.IntegerField(null=True, blank=True)
    creation_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.group_code} - {self.group_name}'

class Customer(models.Model):
    customer_code = models.CharField(max_length=255)
    customer_name = models.CharField(max_length=255, null=True, blank=True)
    customer_group = models.ForeignKey('CustomerGroup', on_delete=models.RESTRICT, null=True)
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    region = models.CharField(max_length=10000, null=True, blank=True)
    ward = models.CharField(max_length=10000, null=True, blank=True)
    specific_address = models.CharField(max_length=10000, null=True, blank=True)
    ########
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=255, null=True, blank=True)
    fax_number = models.CharField(max_length=255, null=True, blank=True)
    tax_code = models.CharField(max_length=255, null=True, blank=True)
    website = models.CharField(max_length=255, null=True, blank=True)
    debt = models.IntegerField(null=True, blank=True)
    total_spending = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.customer_code} - {self.customer_name} - {self.customer_group}'

class SupplierGroup(models.Model):
    group_code = models.CharField(max_length=255)
    group_name = models.CharField(max_length=255, null=True, blank=True)
    notes = models.CharField(max_length=10000, null=True, blank=True)

    def __str__(self):
        return f'{self.group_code} - {self.group_name}'

class Supplier(models.Model):
    supplier_code = models.CharField(max_length=255)
    supplier_name = models.CharField(max_length=255, null=True, blank=True)
    supplier_group = models.ForeignKey('SupplierGroup', on_delete=models.RESTRICT, null=True)
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    region = models.CharField(max_length=10000, null=True, blank=True)
    ward = models.CharField(max_length=10000, null=True, blank=True)
    address_1 = models.CharField(max_length=10000, null=True, blank=True)
    address_2 = models.CharField(max_length=10000, null=True, blank=True)
    ########
    fax_number = models.CharField(max_length=255, null=True, blank=True)
    tax_code = models.CharField(max_length=255, null=True, blank=True)
    website = models.CharField(max_length=255, null=True, blank=True)
    debt = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.supplier_code} - {self.supplier_name} - {self.supplier_group}'

class ProductType(models.Model):
    type_code = models.CharField(max_length=255)
    type_name = models.CharField(max_length=255, null=True, blank=True)
    notes = models.CharField(max_length=10000, null=True, blank=True)
    creation_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.type_code} - {self.type_name}'

class Brand(models.Model):
    brand_code = models.CharField(max_length=255)
    brand_name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f'{self.brand_code} - {self.brand_name}'

class Product(models.Model):
    product_code = models.CharField(max_length=255)
    product_name = models.CharField(max_length=255, null=True, blank=True)
    weight = models.CharField(max_length=255, null=True, blank=True)
    product_type = models.ForeignKey('ProductType', on_delete=models.RESTRICT, null=True)
    brand = models.ForeignKey('Brand', on_delete=models.RESTRICT, null=True)
    barcode = models.CharField(max_length=255, null=True, blank=True)
    unit_of_measurement = models.CharField(max_length=255, null=True, blank=True)
    retail_price = models.IntegerField(null=True, blank=True)
    wholesale_price = models.IntegerField(null=True, blank=True)
    purchase_price = models.IntegerField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    cost_price = models.FloatField(null=True, blank=True)
    initial_stock = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.product_code} - {self.product_name}'

class Order(models.Model):
    order_code = models.CharField(max_length=255)
    customer = models.ForeignKey('Customer', on_delete=models.RESTRICT, null=True)
    order_time = models.DateTimeField(null=True, blank=True)
    delivery_date = models.DateTimeField(null=True, blank=True)
    source = models.CharField(max_length=255, null=True, blank=True)
    payment_method = models.CharField(max_length=255, null=True, blank=True)
    reference = models.CharField(max_length=255, null=True, blank=True)
    order_link = models.CharField(max_length=255, null=True, blank=True)
    total_amount = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f'{self.order_code} - {self.customer}'
    
class OrderLine(models.Model):
    order = models.ForeignKey('Order', on_delete=models.RESTRICT, null=True)
    order_line_code = models.CharField(max_length=255, null=True)
    product = models.ForeignKey('Product', on_delete=models.RESTRICT, null=True)
    quantity = models.IntegerField(null=True, blank=True)
    unit_price = models.IntegerField(null=True, blank=True)
    discount = models.FloatField(null=True, blank=True)
    total_price = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f'{self.order.order_code} - {self.order_line_code} - {self.product.product_code}'


class FeedBack(models.Model):
    email = models.EmailField(max_length=255, null=True, blank=True)
    message = models.CharField(max_length=100000, null=True)

    def __str__(self):
        return f'{self.email} - {self.message}'