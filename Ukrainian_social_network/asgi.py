import os
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

from django.core.asgi import get_asgi_application
from communications.routing import websocket_urlpatterns  # Импортируйте маршруты WebSocket

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Ukrainian_social_network.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns  # Передайте маршруты WebSocket из communications.routing
        )
    ),
})
