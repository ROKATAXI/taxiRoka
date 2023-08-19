# your_project/routing.py

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path

from chat.consumers import ChatConsumer  # ChatConsumer는 실제 컨슈머 클래스의 경로에 맞게 수정해야 합니다.

application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path("ws/some_path/", ChatConsumer.as_asgi()),
            # 다른 컨슈머와 경로도 추가할 수 있습니다.
        ])
    ),
})
