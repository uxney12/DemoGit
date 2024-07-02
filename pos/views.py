from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import CustomerGroup, Customer, SupplierGroup, Supplier, ProductType, Brand, Product, Order, OrderLine
from django.utils.timezone import now as timezone_now
import pandas as pd 
import os 
import time
from datetime import datetime
import json
from django.http import JsonResponse
from django.shortcuts import redirect



def index(request):
    """View function for home page of site."""

    num_customer_groups = CustomerGroup.objects.all().count()
    num_customers = Customer.objects.all().count()
    num_supplier_groups = SupplierGroup.objects.all().count()
    num_suppliers = Supplier.objects.all().count()
    num_product_types = ProductType.objects.all().count()
    num_brands = Brand.objects.all().count()
    num_products = Product.objects.all().count()
    num_orders = Order.objects.all().count()
    num_order_lines = OrderLine.objects.all().count()

    context = {
        'num_customer_groups': num_customer_groups,
        'num_customers': num_customers,
        'num_supplier_groups': num_supplier_groups,
        'num_suppliers': num_suppliers,
        'num_product_types': num_product_types,
        'num_brands': num_brands,
        'num_products': num_products,
        'num_orders': num_orders,
        'num_order_lines': num_order_lines,
    }
    return render(request, 'index.html', context=context)


############################################################
############################################################
############################################################


@csrf_exempt 
def upload_customer_group(request):
    print("1XXXXXXXXXXXXXXXXXXXXX")
    if request.method == 'POST' and request.FILES.get('file'):
        print("2XXXXXXXXXXXXXXXXXXXXX")
        uploaded_file = request.FILES['file'] 
        excel_data = uploaded_file.read()
        df = pd.read_excel(excel_data)
        required_columns = ['Mã nhóm', 'Tên nhóm', 'Loại', 'Mô tả', 'Số lượng khách hàng', 'Ngày tạo']
        
        if not all(col in df.columns for col in required_columns):
            messages.error(request, 'Thiếu các cột bắt buộc trong tệp Excel.')
            return redirect('/customer_group')
        
        for index, row in df.iterrows():
            CustomerGroup.objects.create(
                group_code=row['Mã nhóm'],
                group_name=row['Tên nhóm'],
                group_type=row['Loại'],
                description=row['Mô tả'],
                customer_count=row['Số lượng khách hàng'],
                creation_date=row['Ngày tạo'],
            )
        print("3XXXXXXXXXXXXXXXXXXXXX")
        return JsonResponse({'message': 'Dữ liệu đã được tải lên từ Excel thành công!'})
    
    return JsonResponse({'error': 'Bad request'}, status=400)
        


############################################################
############################################################
############################################################


current_time = datetime.now().date()
@csrf_exempt
def create_customer_group(request):
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        group_code = request.POST.get('group_code') or body.get('group_code')
        group_name = request.POST.get('group_name') or body.get('group_name')
        group_type = request.POST.get('group_type') or body.get('group_type')
        description = request.POST.get('description') or body.get('description')
        creation_date = current_time
        CustomerGroup.objects.create(
            group_code=group_code,
            group_name=group_name,
            group_type=group_type,
            description=description,
            creation_date=creation_date,
        )        
        return JsonResponse({'status': 'success', 'group_code': group_code})
    context = {
        'current_time': current_time
        }
    return render(request, 'pos/create_customer_group_form.html', context)


creation_date = datetime.now().date()
@csrf_exempt
def create_customer(request):
    last_customer = Customer.objects.last()

    if last_customer and last_customer.customer_code.startswith('KH') and last_customer.customer_code[2:].isdigit():
        last_customer_index = int(last_customer.customer_code[2:])
    else:
        last_customer_index = 0
    new_customer_id = f'KH{last_customer_index + 1:05d}'

    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        customer_name = request.POST.get('customer_name') or body.get('customer_name')
        customer_group_value = request.POST.get('customer_group') or body.get('customer_group')
        customer_group = customer_group_value.split('-')[0].strip() if customer_group_value else None
        phone_number = request.POST.get('phone_number') or body.get('phone_number')
        email = request.POST.get('email') or body.get('email')
        region = request.POST.get('region') or body.get('region')
        ward = request.POST.get('ward') or body.get('ward')
        specific_address = request.POST.get('specific_address') or body.get('specific_address')
        birth_date = request.POST.get('birth_date') or body.get('birth_date')
        birth_date = parse_date(birth_date) if birth_date else None
        gender = request.POST.get('gender') or body.get('gender')
        fax_number = request.POST.get('fax_number') or body.get('fax_number')
        tax_code = request.POST.get('tax_code') or body.get('tax_code')
        website = request.POST.get('website') or body.get('website')
        debt = request.POST.get('debt') or body.get('debt') or None
        total_spending = request.POST.get('total_spending') or body.get('total_spending') or None

        Customer.objects.create(
            customer_code=new_customer_id,
            customer_name=customer_name,
            customer_group=CustomerGroup.objects.filter(group_code=customer_group).last(),
            phone_number=phone_number,
            email=email,
            region=region,
            ward=ward,
            specific_address=specific_address,
            birth_date=birth_date,
            gender=gender,
            fax_number=fax_number,
            tax_code=tax_code,
            website=website,
            debt=debt,
            total_spending=total_spending
        )   
        return JsonResponse({'status': 'success', 'customer_code': new_customer_id})

    customer_group = CustomerGroup.objects.all()
    context = {
        'customer_group': customer_group,
        'new_customer_id': new_customer_id,
        'creation_date': creation_date,
    }
    return render(request, 'pos/create_customer_form.html', context)


@csrf_exempt
def create_supplier_group(request):
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        group_code = request.POST.get('group_code') or body.get('group_code')
        group_name = request.POST.get('group_name') or body.get('group_name')
        notes = request.POST.get('notes') or body.get('notes')
        SupplierGroup.objects.create(
            group_code=group_code,
            group_name=group_name,
            notes=notes,
        ) 
        return JsonResponse({'status': 'success', 'group_code': group_code})       
    return render(request, 'pos/create_supplier_group_form.html')


@csrf_exempt
def create_supplier(request):
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        supplier_code = request.POST.get('supplier_code') or body.get('supplier_code')
        supplier_name = request.POST.get('supplier_name') or body.get('supplier_name')
        supplier_group_data = request.POST.get('supplier_group') or body.get('supplier_group')
        if supplier_group_data:
            supplier_group = supplier_group_data.split('-')[0].strip()
        else:
            supplier_group = None
        phone_number = request.POST.get('phone_number') or body.get('phone_number')
        email = request.POST.get('email') or body.get('email')
        region = request.POST.get('region') or body.get('region')
        ward = request.POST.get('ward') or body.get('ward')
        address_1 = request.POST.get('address_1') or body.get('address_1')
        address_2 = request.POST.get('address_2') or body.get('address_2')
        ########
        fax_number = request.POST.get('fax_number') or body.get('fax_number')
        tax_code = request.POST.get('tax_code') or body.get('tax_code')
        website = request.POST.get('website') or body.get('website')
        debt = request.POST.get('debt') or body.get('debt') or None
        Supplier.objects.create(
            supplier_code=supplier_code,
            supplier_name=supplier_name,
            supplier_group=SupplierGroup.objects.filter(group_code=supplier_group).last(),
            phone_number=phone_number,
            email=email,
            region=region,
            ward=ward,
            address_1=address_1,
            address_2=address_2,
            fax_number=fax_number,
            tax_code=tax_code,
            website=website,
            debt=debt
        )   
    supplier_group = SupplierGroup.objects.all()
    context = {
        'supplier_group': supplier_group,
        }
    return render(request, 'pos/create_supplier_form.html', context)


current_time = datetime.now().date()
@csrf_exempt
def create_product_type(request):
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        type_code = request.POST.get('type_code') or body.get('type_code')
        type_name = request.POST.get('type_name') or body.get('type_name')
        notes = request.POST.get('notes') or body.get('notes')
        creation_date = current_time or body.get('creation_date')
        ProductType.objects.create(
            type_code=type_code,
            type_name=type_name,
            notes=notes,
            creation_date=creation_date
        )     
        return JsonResponse({'status': 'success', 'type_code': type_code})   
    context = {
        'current_time': current_time,
        }
    return render(request, 'pos/create_product_type_form.html', context)


@csrf_exempt
def create_brand(request):
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        brand_code = request.POST.get('brand_code') or body.get('brand_code')
        brand_name = request.POST.get('brand_name') or body.get('brand_name')
        Brand.objects.create(
            brand_code=brand_code,
            brand_name=brand_name
        )        
        return JsonResponse({'status': 'success', 'brand_code': brand_code}) 
    return render(request, 'pos/create_brand_form.html')


creation_date = datetime.now().date()
@csrf_exempt
def create_product(request):
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        product_code = request.POST.get('product_code') or body.get('product_code') 
        product_name = request.POST.get('product_name') or body.get('product_name') 
        weight = request.POST.get('weight') or body.get('weight') 
        product_type_data = request.POST.get('product_type') or body.get('product_type') 
        if product_type_data:
            product_type = product_type_data.split('-')[0].strip()
        else:
            product_type = None
        brand_data = request.POST.get('brand') or body.get('brand')
        if brand_data:
            brand = brand_data.split('-')[0].strip()
        else:
            brand = None
        barcode = request.POST.get('barcode') or body.get('barcode') 
        unit_of_measurement = request.POST.get('unit_of_measurement') or body.get('unit_of_measurement') 
        retail_price = request.POST.get('retail_price') or body.get('retail_price') or None
        wholesale_price = request.POST.get('wholesale_price') or body.get('wholesale_price') or None
        purchase_price = request.POST.get('purchase_price') or body.get('purchase_price') or None
        image = request.POST.get('image') or body.get('image') 
        cost_price = request.POST.get('cost_price') or body.get('cost_price') or None
        initial_stock = request.POST.get('initial_stock') or body.get('initial_stock') or None
        Product.objects.create(
            product_code=product_code,
            product_name=product_name,
            weight=weight,
            product_type=ProductType.objects.filter(type_code=product_type).last(),
            brand=Brand.objects.filter(brand_code=brand).last(),
            barcode=barcode,
            unit_of_measurement=unit_of_measurement,
            retail_price=retail_price,
            wholesale_price=wholesale_price,
            purchase_price=purchase_price,
            image=image,
            cost_price=cost_price,
            initial_stock=initial_stock
        )   
        print(request.body)
    product_type = ProductType.objects.all()
    brand = Brand.objects.all()
    context = {
        'product_type': product_type,
        'brand': brand,
        'creation_date': creation_date,
        }
    return render(request, 'pos/create_product_form.html', context)


@csrf_exempt
def create_order(request):
    current_time = datetime.now() 

    form_values = request.POST.copy()
    last_order = Order.objects.last()

    if last_order and last_order.order_code.startswith('ORD') and last_order.order_code[3:].isdigit():
        last_order_index = int(last_order.order_code[3:])
    else:
        last_order_index = 0
        
    new_order_id = f'ORD{last_order_index + 1:06d}'
    
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        order_code = new_order_id 
        order_time = current_time 
        delivery_date = request.POST.get('delivery_date') or body.get('delivery_date') 
        delivery_date = parse_date(delivery_date) if delivery_date else None
        
        customer_data = request.POST.get('customer') or body.get('customer')
        if customer_data:
            customer = customer_data.split('-')[0].strip()
        else:
            customer = None
        
        source = request.POST.get('source') or body.get('source') 
        payment_method = request.POST.get('payment_method') or body.get('payment_method') 
        reference = request.POST.get('reference') or body.get('reference') 
        order_link = request.POST.get('order_link') or body.get('order_link') 
        total_amount = request.POST.get('total_amount') or body.get('total_amount') 

        customer_flt = Customer.objects.filter(customer_code=customer).last()
        order = Order.objects.create(
            order_code=order_code,
            order_time=order_time,
            delivery_date=delivery_date,
            customer=customer_flt,
            source=source,
            payment_method=payment_method,
            reference=reference,
            order_link=order_link,
            total_amount=total_amount
        )
        
        order_lines = body.get('order_lines', [])
        
        order_line_codes = []
        products = []
        quantities = []
        unit_prices = []
        discounts = []
        total_prices = []

        for line in order_lines:
            order_line_codes.append(line.get('order_line_code', ''))
            products.append(line.get('product', ''))
            quantities.append(line.get('quantity', ''))
            unit_prices.append(line.get('unit_price', ''))
            discounts.append(line.get('discount', ''))
            total_prices.append(line.get('total_price', ''))

        if not order_lines:
            order_line_codes = form_values.getlist('order_line_code', [])
            products = form_values.getlist('product', [])
            quantities = form_values.getlist('quantity', [])
            unit_prices = form_values.getlist('unit_price', [])
            discounts = form_values.getlist('discount', [])
            total_prices = form_values.getlist('total_price', [])

        for order_line_code, product, quantity, unit_price, discount, total_price in zip(order_line_codes, products, quantities, unit_prices, discounts, total_prices):
            product_code = product.split('-')[0].strip()
            product_flt = Product.objects.filter(product_code=product_code).last()
            unit_price = float(unit_price) if unit_price else 0.0  
            OrderLine.objects.create(
                order=order,
                order_line_code=order_line_code,
                product=product_flt,
                quantity=quantity,
                unit_price=unit_price,
                discount=discount,
                total_price=total_price
            )
        print(request.body)
    
    last_customer = Customer.objects.last()

    if last_customer and last_customer.customer_code.startswith('KH') and last_customer.customer_code[2:].isdigit():
        last_customer_index = int(last_customer.customer_code[2:])
    else:
        last_customer_index = 0
    new_customer_id = f'KH{last_customer_index + 1:05d}'

    customers = Customer.objects.all()
    products = Product.objects.all()
    customer_group = CustomerGroup.objects.all()     
    # customers = list(Customer.objects.all().values('customer_code', 'customer_name'))
    # products = list(Product.objects.all().values('product_code', 'product_name', 'retail_price'))
    # customer_group = list(CustomerGroup.objects.all().values('group_code', 'group_name'))    
    context = {
        'current_time': current_time,
        'customers': customers,
        'products': products,
        'new_order_id': new_order_id,
        'new_customer_id': new_customer_id,
        'customer_group': customer_group
    }
    print(context)
    return render(request, 'pos/create_order_form.html', context)


############################################################
############################################################
############################################################


def list_customer_group(request):
    customer_group = CustomerGroup.objects.all()
    context = {
        'customer_group': customer_group
    }
    return render(request, 'pos/list_customer_group.html', context)


def list_customer(request):
    customer= Customer.objects.all()
    context = {
        'customer': customer
    }
    return render(request, 'pos/list_customer.html', context)


def list_supplier_group(request):
    supplier_group = SupplierGroup.objects.all()
    context = {
        'supplier_group': supplier_group
    }
    return render(request, 'pos/list_supplier_group.html', context)

def list_supplier(request):
    supplier = Supplier.objects.all()
    context = {
        'supplier': supplier
    }
    return render(request, 'pos/list_supplier.html', context)

def list_product_type(request):
    product_type = ProductType.objects.all()
    context = {
        'product_type': product_type
    }
    return render(request, 'pos/list_product_type.html', context)


def list_brand(request):
    brand = Brand.objects.all()
    context = {
        'brand': brand
    }
    return render(request, 'pos/list_brand.html', context)


def list_product(request):
    product = Product.objects.all()
    context = {
        'product': product
    }
    return render(request, 'pos/list_product.html', context)


def list_order(request):
    order = Order.objects.all()
    context = {
        'order': order
    }
    return render(request, 'pos/list_order.html', context)


############################################################
############################################################
############################################################


def customer_detail_view(request, customer_code):
    customer = get_object_or_404(Customer, customer_code=customer_code)
    orders = Order.objects.filter(customer=customer)
    context = {
        'customer': customer, 
        'orders': orders
    }
    return render(request, 'pos/detail_customer.html', context)


############################################################
############################################################
############################################################


def customer_delete(request, customer_code):
    customer = get_object_or_404(Customer, customer_code=customer_code)
    if request.method == 'POST':
        customer.delete()
        return redirect('/customer')

    return render(request, 'pos/customer_confirm_delete.html', {'customer': customer})