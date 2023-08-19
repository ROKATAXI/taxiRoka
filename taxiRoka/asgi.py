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
from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from django.urls import path
from apps.chat.routing import websocket_urlpatterns
from apps.chat.consumers import ChatConsumer

django_asgi_app = get_asgi_application()

class WebSocketAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        # Get the user from the Django authentication middleware
        scope['user'] = await database_sync_to_async(self.get_user)(scope)

        return await super().__call__(scope, receive, send)

    def get_user(self, scope):
        return AnonymousUser() if scope.get('user', None) is None else scope['user']


application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(websocket_urlpatterns))
        ),
    }
)
