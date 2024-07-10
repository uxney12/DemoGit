from django.urls import path
from . import views

app_name = 'pos'

urlpatterns = [
    path('', views.index, name='index'),

    ###############################################################################

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

    path('customer/<str:customer_code>/', views.customer_detail, name='customer_detail'),
    path('customer_group/<str:group_code>/', views.customer_group_detail, name='customer_group_detail'),
    path('supplier_group/<str:group_code>/', views.supplier_group_detail, name='supplier_group_detail'),
    path('supplier/<str:supplier_code>/', views.supplier_detail, name='supplier_detail'),
    path('brand/<str:brand_code>/', views.brand_detail, name='brand_detail'),
    path('product_type/<str:type_code>/', views.product_type_detail, name='product_type_detail'),
    path('product/<str:product_code>/', views.product_detail, name='product_detail'),
    path('order/<str:order_code>/', views.order_detail, name='order_detail'),

    ###############################################################################

    path('customer/<str:customer_code>/delete/', views.customer_delete, name='customer_delete'),
    path('customer_group/<str:group_code>/delete/', views.customer_group_delete, name='customer_group_delete'),
    path('supplier_group/<str:group_code>/delete/', views.supplier_group_delete, name='supplier_group_delete'),
    path('supplier/<str:supplier_code>/delete/', views.supplier_delete, name='supplier_delete'),
    path('brand/<str:brand_code>/delete/', views.brand_delete, name='brand_delete'),
    path('product_type/<str:type_code>/delete/', views.product_type_delete, name='product_type_delete'),
    path('product/<str:product_code>/delete/', views.product_delete, name='product_delete'),
    path('order/<str:order_code>/delete/', views.order_delete, name='order_delete'),

    ###############################################################################

    path('customer_group_upload', views.upload_customer_group, name='upload_customer_group'),
    path('customer_upload', views.upload_customer, name='upload_customer'),
    path('supplier_group_upload', views.upload_supplier_group, name='upload_supplier_group'),
    path('supplier_upload', views.upload_supplier, name='upload_supplier'),
    path('brand_upload', views.upload_brand, name='upload_brand'),
    path('product_type_upload', views.upload_product_type, name='upload_product_type'),
    path('product_upload', views.upload_product, name='upload_product'),
    path('order_upload', views.upload_order, name='upload_order'),
]

