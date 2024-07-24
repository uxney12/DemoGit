from .models import CustomerGroup, Customer, SupplierGroup, Supplier, ProductType, Brand, Product, Order, OrderLine
from rest_framework import serializers

# Chuyển đổi dữ liệu của mô hình thành định dạng JSON (hoặc định dạng khác) mà các API có thể sử dụng. 
# Serializer giúp kết nối giữa các mô hình Django và các dữ liệu JSON mà frontend hoặc các hệ thống khác có thể dễ dàng sử dụng và hiểu.


class CustomerGroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomerGroup
        fields = '__all__'


class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class SupplierGroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SupplierGroup
        fields = '__all__'


class SupplierSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'


class ProductTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProductType
        fields = '__all__'


class BrandSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class OrderLineSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OrderLine
        fields = '__all__'