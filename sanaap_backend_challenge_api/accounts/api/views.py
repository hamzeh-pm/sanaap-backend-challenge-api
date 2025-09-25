from django.contrib.auth.models import Group
from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView

from sanaap_backend_challenge_api.accounts.api.serializers import (
    RoleBasedTokenObtainPairSerializer,
)
from sanaap_backend_challenge_api.accounts.api.serializers import RoleResponseSerializer
from sanaap_backend_challenge_api.accounts.permissions import CanViewRoles


class RoleBasedTokenObtainPairView(TokenObtainPairView):
    serializer_class = RoleBasedTokenObtainPairSerializer


class RoleListView(generics.ListAPIView):
    queryset = Group.objects.all()
    serializer_class = RoleResponseSerializer
    permission_classes = [CanViewRoles]
