from django.urls import path
from . import views

app_name = 'pos'

urlpatterns = [
    path('', views.index, name='index'),
    path('customer_group/create', views.create_customer_group, name='create_customer_group'),
    path('customer/create', views.create_customer, name='create_customer'),
    path('supplier_group/create', views.create_supplier_group, name='create_supplier_group'),
    path('supplier/create', views.create_supplier, name='create_supplier'),
    path('product_type/create', views.create_product_type, name='create_product_type'),
    path('brand/create', views.create_brand, name='create_brand'),
    path('product/create', views.create_product, name='create_product'),
    path('order/create', views.create_order, name='create_order'),
    ###############################################################################
    path('customer_group', views.list_customer_group, name='list_customer_group'),
    path('customer', views.list_customer, name='list_customer'),
    path('supplier_group', views.list_supplier_group, name='list_supplier_group'),
    path('supplier', views.list_supplier, name='list_supplier'),
    path('product_type', views.list_product_type, name='list_product_type'),
    path('brand', views.list_brand, name='list_brand'),
    path('product', views.list_product, name='list_product'),
    path('order', views.list_order, name='list_order'),
    ###############################################################################
    path('customer/<str:customer_code>/', views.customer_detail_view, name='customer_detail'),
    ###############################################################################
    path('customer/<str:customer_code>/delete/', views.customer_delete, name='customer_delete'),
    ###############################################################################
    path('customer_group_upload', views.upload_customer_group, name='upload_customer_group'),
    
]

