#asgi.py
import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

import pos.routing


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sapo.settings')

application = get_asgi_application()
application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket": AuthMiddlewareStack(
    URLRouter(
      pos.routing.websocket_urlpatterns
    )
  )
})