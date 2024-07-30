# consumer.py
import json
import re
import time
from datetime import datetime
from .models import CustomerGroup, Customer, SupplierGroup, Supplier, ProductType, Brand, Product, Order, OrderLine, FeedBack, Message
from channels.generic.websocket import AsyncWebsocketConsumer 
from asgiref.sync import sync_to_async 

class ChatConsumer(AsyncWebsocketConsumer):
    # Xử lý các kết nối WebSocket cho một hệ thống chat 
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        
        await self.channel_layer.group_add(
        self.room_group_name,
        self.channel_name
        )

        await self.accept()

    # Xóa kết nối khỏi nhóm phòng chat khi người dùng ngắt kết nối
    async def disconnect(self, close_code):
        
        await self.channel_layer.group_discard(
        self.room_group_name,
        self.channel_name
    )

    # Nhận tin nhắn và gửi tin nhắn
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        username = data['username']
        room = data['room']

        await self.save_message(username, room, message)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username
            }
        )
        
        # Phản hồi cho lời chào
        greeting_pattern = re.compile(r'\b(Chào|Hi|Hello|Good morning|Good afternoon|Good evening)\b', re.IGNORECASE)
        old_order_pattern = re.compile(r'\b(Lịch sử|Cũ)\b', re.IGNORECASE)
        new_order_pattern = re.compile(r'\b(Đặt)\b', re.IGNORECASE)
        customer_code_pattern = re.compile(r'\b(KH\d+.*)\b', re.IGNORECASE)
        order_message_pattern = re.compile(
            r'(?P<customer_name>[\w\s]+)\s*-\s*'  
            r'(?P<products>(?:[\w\d]+\s*\|\s*)*[\w\d]+)\s*-\s*'  
            r'(?P<quantities>(?:\d+\s*\|\s*)*\d+)\s*-\s*'  
            r'(?P<payment_method>[\w\s]+)',  
            re.IGNORECASE
        )
        thank_you_pattern = re.compile(r'\b(Thank|Cảm ơn)\b', re.IGNORECASE)

        if greeting_pattern.search(message):
            print("Greeting detected.")
            greeting_response = "Chào bạn, tôi có thể giúp được gì?"
            await self.save_message('admin', room, greeting_response)
            await self.send_message_to_group(greeting_response, 'admin')
            return  
        
        if old_order_pattern.search(message):
            print("Old order pattern detected.")
            old_order_response = "Mã khách hàng của bạn là gì?"
            await self.save_message('admin', room, old_order_response)
            await self.send_message_to_group(old_order_response, 'admin')
            return
        
        if customer_code_pattern.search(message):
            customer_code = customer_code_pattern.search(message).group(0)
            customer = await sync_to_async(Customer.objects.filter(customer_code=customer_code).first)()
            
            if not customer:
                await self.save_message('admin', room, "Khách hàng không tồn tại.")
                await self.send_message_to_group("Khách hàng không tồn tại.", 'admin')
                return

            orders = await sync_to_async(lambda: list(Order.objects.select_related('customer__customer_group').filter(customer=customer)))()

            if not orders:
                await self.save_message('admin', room, "Khách hàng chưa có đơn hàng nào.")
                await self.send_message_to_group("Khách hàng chưa có đơn hàng nào.", 'admin')
                return

            order_lines_dict = {}
            
            for order in orders:
                order_lines = await sync_to_async(lambda: list(OrderLine.objects.select_related('product').filter(order=order)))()
                order_lines_dict[order] = order_lines

            order_list = ""
            for order in orders:
                order_lines = order_lines_dict[order]
                order_lines_str = "\n".join([f"STT: {line.order_line_code} + Sản phẩm: {line.product} + Số lượng: {line.quantity} + Đơn giá: {line.unit_price} + Chiết khấu: {line.discount} + Thành tiền: {line.total_price}" for line in order_lines])
                order_list += (
                    f"- Mã đơn hàng: {order.order_code}\n- Tên khách hàng: {order.customer.customer_name}\n- Thời gian: {order.order_time}\n- Phương thức thanh toán: {order.payment_method}\n- Tổng tiền: {order.total_amount}\n"
                    f"{order_lines_str}\n\n"
                )
            
            order_response = (
                "Đây là danh sách các đơn hàng và sản phẩm:\n\n"
                f"{order_list}\n"
            )
            formatted_order_response = order_response.replace('\n', '<br>')
            await self.save_message('admin', room, order_response)
            await self.send_message_to_group(formatted_order_response, 'admin')
            return

        if new_order_pattern.search(message):
            print("New order pattern detected.")
            
            products = await sync_to_async(lambda: list(Product.objects.all()))()
            product_list = "\n".join([f"{product.product_code} - {product.product_name} - {product.retail_price}" for product in products])
            product_response = (
                "Đây là danh sách các sản phẩm:\n"
                f"{product_list}\n"
                "Bạn muốn đặt mặt hàng gì?\n"
                "Vui lòng điền thêm cú pháp sau: TÊN KHÁCH HÀNG - MÃ SẢN PHẨM 1 | MÃ SẢN PHẨM 2 - SỐ LƯỢNG 1 | SỐ LƯỢNG 2  - PHƯƠNG THỨC THANH TOÁN "
            )
            formatted_product_response = product_response.replace('\n', '<br>')
            await self.save_message('admin', room, product_response)
            await self.send_message_to_group(formatted_product_response, 'admin')
            return

        order_match = order_message_pattern.search(message)
        if order_match:
            customer_name = order_match.group('customer_name').strip()
            products = order_match.group('products').split('|')
            quantities = order_match.group('quantities').split('|')
            payment_method = order_match.group('payment_method')

            products = [product.strip() for product in products]
            quantities = [quantity.strip() for quantity in quantities]
            
            customer_exists = await sync_to_async(Customer.objects.select_related('customer_group').filter(customer_name=customer_name).first)()
            if customer_exists:
                customer = customer_exists
            else: 
                last_customer = await sync_to_async(lambda: Customer.objects.last())()

                if last_customer and last_customer.customer_code.startswith('KH') and last_customer.customer_code[2:].isdigit():
                    last_customer_index = int(last_customer.customer_code[2:])
                else:
                    last_customer_index = 0
                new_customer_code = f'KH{last_customer_index + 1:05d}'
                customer = await sync_to_async(Customer.objects.create)(
                    customer_code=new_customer_code,
                    customer_name=customer_name,
                )

            total_price = 0
            order_lines = []
            order_line_counter = 1

            for product_code, quantity_str in zip(products, quantities):
                quantity = int(quantity_str)
                product = await sync_to_async(lambda: Product.objects.filter(product_code=product_code).first())()

                if not product:
                    error_message = f"Sản phẩm {product_code} không tồn tại."
                    await self.save_message('admin', room, error_message)
                    await self.send_message_to_group(error_message, 'admin')
                    return

                unit_price = product.retail_price
                line_total_price = unit_price * quantity
                total_price += line_total_price

                order_line_code = f'L{order_line_counter:03d}'  
                order_line_counter += 1

                order_lines.append({
                    'order_line_code': order_line_code,
                    'product': product,
                    'quantity': quantity,
                    'unit_price': unit_price,
                    'line_total_price': line_total_price,
                })

            last_order = await sync_to_async(lambda: Order.objects.last())()
    
            if last_order and last_order.order_code.startswith('ORD') and last_order.order_code[3:].isdigit():
                last_order_index = int(last_order.order_code[3:])
            else:
                last_order_index = 0

            new_order_code = f'ORD{last_order_index + 1:06d}'
            print(f"Mã đơn hàng mới: {new_order_code}")

            order = await sync_to_async(Order.objects.create)(
                order_code=new_order_code,
                customer=customer,
                order_time=datetime.now(),
                payment_method=payment_method,
                total_amount=total_price
            )

            for line in order_lines:
                await sync_to_async(OrderLine.objects.create)(
                order=order,
                order_line_code=line['order_line_code'],
                product=line['product'],
                quantity=line['quantity'],
                unit_price=line['unit_price'],
                total_price=line['line_total_price']
            )

            order_response = (
                f"Đơn hàng của bạn đã được đặt thành công!\n"
                f"Mã đơn hàng: {new_order_code}\n"
                f"Tên khách hàng: {customer_name}\n"
            )

            for line in order_lines:
                order_response += (
                    f"STT: {line['order_line_code']}\n"
                    f"- Sản phẩm: {line['product'].product_name}\n"
                    f"- Số lượng: {line['quantity']}\n"
                    f"- Đơn giá: {line['unit_price']:.2f} VND\n"
                    f"- Thành tiền: {line['line_total_price']:.2f} VND\n"
                )

            order_response += (
                f"Tổng giá: {total_price:.2f} VND\n"
                f"Phương thức thanh toán: {payment_method}\n"
                f"Cảm ơn bạn đã mua hàng!"
            )

            formatted_order_response = order_response.replace('\n', '<br>')
            await self.save_message('admin', room, order_response)
            await self.send_message_to_group(formatted_order_response, 'admin')
            return

        if thank_you_pattern.search(message):
            print("Thank you detected.")
            thank_you_response = "Không có gì, rất vui được giúp bạn!"
            await self.save_message('admin', room, thank_you_response)
            await self.send_message_to_group(thank_you_response, 'admin')
            return

    # Tạo nhóm và gửi tin nhắn đến nhóm
    async def send_message_to_group(self, message, username):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username
            }
        )
            

    # Phát tin nhắn đến tất cả các người dùng hiện có trong cùng một phòng chat  
    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))

    # Các tin nhắn được gửi qua WebSocket sẽ được lưu vào cơ sở dữ liệu
    @sync_to_async
    def save_message(self, username, room, message):
        Message.objects.create(username=username, room=room, content=message)