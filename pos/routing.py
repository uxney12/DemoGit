# routing.py
# Cấu hình URL cho các kết nối WebSocket trong ứng dụng
from django.urls import path
from . import consumers

websocket_urlpatterns = [
  path('ws/<str:room_name>/', consumers.ChatConsumer.as_asgi()),
]

