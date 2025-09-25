from rest_framework_simplejwt.views import TokenObtainPairView
from sanaap_backend_challenge_api.accounts.api.serializers import (
    RoleBasedTokenObtainPairSerializer,
)


class RoleBasedTokenObtainPairView(TokenObtainPairView):
    serializer_class = RoleBasedTokenObtainPairSerializer
