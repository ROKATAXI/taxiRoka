"""
ASGI config for taxiRoka project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taxiRoka.settings')
django.setup()
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from django.urls import path
from apps.chat.routing import websocket_urlpatterns
from apps.chat.consumers import ChatConsumer

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": URLRouter([
        # 이 부분에 웹소켓 라우팅을 추가해주세요.
        # ChatConsumer를 포함하여 필요한 라우팅을 정의하세요.
        path("ws/chat/<str:room_uuid>/", ChatConsumer.as_asgi()),
        ]),
    }
)
