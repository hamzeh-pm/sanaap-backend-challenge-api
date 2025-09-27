import os

from channels.routing import ProtocolTypeRouter
from channels.routing import URLRouter
from django.core.asgi import get_asgi_application

from sanaap_backend_challenge_api.documents import (
    routing as document_routing,  # noqa: E402
)
from sanaap_backend_challenge_api.utils.ws_middlewares import JWTAuthMiddlewareStack

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings.local")

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": JWTAuthMiddlewareStack(
            URLRouter(document_routing.websocket_urlpatterns)
        ),
    }
)
