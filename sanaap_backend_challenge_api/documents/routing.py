from django.urls import path
from sanaap_backend_challenge_api.documents import consumers

websocket_urlpatterns = [
    path("ws/documents/", consumers.DocumentConsumer.as_asgi()),
]
