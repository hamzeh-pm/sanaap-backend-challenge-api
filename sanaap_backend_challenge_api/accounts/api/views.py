from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from sanaap_backend_challenge_api.accounts import permissions
from sanaap_backend_challenge_api.accounts.api import serializers as account_serializers
from sanaap_backend_challenge_api.accounts.services import AccountService
from django.contrib.auth.models import Group


User = get_user_model()


class RoleBasedTokenObtainPairView(TokenObtainPairView):
    serializer_class = account_serializers.RoleBasedTokenObtainPairSerializer


class RoleListView(generics.ListAPIView):
    queryset = Group.objects.all()
    serializer_class = account_serializers.RoleResponseSerializer
    permission_classes = [permissions.CanViewRoles]


class UserViewset(viewsets.ViewSet):
    def list(self, request):
        data = User.objects.filter(is_active=True).exclude(is_superuser=True)
        serializer = account_serializers.UserResponseSerializer(data, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        user = get_object_or_404(User, pk=pk, is_active=True)
        serializer = account_serializers.UserResponseSerializer(user)
        return Response(serializer.data)

    def create(self, request):
        serializer = account_serializers.UserRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        account_service = AccountService(User, Group)
        user = account_service.create_user(
            username=serializer.validated_data["username"],
            password=serializer.validated_data["password"],
        )
        response_serializer = account_serializers.UserResponseSerializer(user)
        return Response(response_serializer.data, status=201)

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            permission_classes = [permissions.CanViewUsers]
        elif self.action in ["create", "update", "partial_update", "destroy"]:
            permission_classes = [permissions.CanManageUsers]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]
