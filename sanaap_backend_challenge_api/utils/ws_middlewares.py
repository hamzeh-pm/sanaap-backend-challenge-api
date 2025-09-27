import jwt
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.conf import settings
from django.db import close_old_connections
from channels.middleware import BaseMiddleware
from channels.auth import AuthMiddlewareStack
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from urllib.parse import parse_qs
import logging

logger = logging.getLogger(__name__)
User = get_user_model()


class JWTAuthMiddleware(BaseMiddleware):
    """
    Custom middleware to authenticate WebSocket connections using JWT tokens.
    """

    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        # Close old database connections to prevent usage of timed out connections
        close_old_connections()

        # Get the token from query string
        query_string = scope.get("query_string", b"").decode()
        query_params = parse_qs(query_string)
        token = query_params.get("token", [None])[0]

        # Set default user to AnonymousUser
        scope["user"] = AnonymousUser()

        if token:
            try:
                # Validate the token
                UntypedToken(token)

                # Decode the token to get user info
                decoded_data = jwt.decode(
                    token, settings.SECRET_KEY, algorithms=["HS256"]
                )

                # Get user from token
                user_id = decoded_data.get("user_id")
                if user_id:
                    user = await self.get_user(user_id)
                    if user:
                        scope["user"] = user
                        logger.info(f"WebSocket authenticated user: {user.username}")
                    else:
                        logger.warning(f"User not found for ID: {user_id}")

            except (InvalidToken, TokenError, jwt.ExpiredSignatureError) as e:
                logger.warning(f"WebSocket JWT authentication failed: {e}")
            except Exception as e:
                logger.error(f"WebSocket authentication error: {e}")

        return await super().__call__(scope, receive, send)

    async def get_user(self, user_id):
        """Get user from database asynchronously"""
        try:
            from django.contrib.auth import get_user_model

            User = get_user_model()
            return await User.objects.aget(pk=user_id)
        except User.DoesNotExist:
            return None


def JWTAuthMiddlewareStack(inner):
    """
    Custom WebSocket middleware stack that uses JWT authentication
    """
    return JWTAuthMiddleware(AuthMiddlewareStack(inner))
