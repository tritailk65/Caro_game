from django.urls import re_path
from . import game_consumer
from . import service_consumer

websocket_urlpatterns = [
    re_path(r'ws/game-socket/', game_consumer.GameConsumer.as_asgi()),
    re_path(r'ws/service-socket', service_consumer.ServiceConsumer.as_asgi())
]