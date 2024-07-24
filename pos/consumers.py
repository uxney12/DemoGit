# consumer.py
import json

from channels.generic.websocket import AsyncWebsocketConsumer 
from asgiref.sync import sync_to_async 
from .models import Message

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

  # Xử lý việc nhận và gửi tin nhắn
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