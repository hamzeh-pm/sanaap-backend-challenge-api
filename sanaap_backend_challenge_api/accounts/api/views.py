from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from sanaap_backend_challenge_api.accounts import permissions
from sanaap_backend_challenge_api.accounts.api import serializers as account_serializers
from sanaap_backend_challenge_api.accounts.services import AccountService

User = get_user_model()


class RoleBasedTokenObtainPairView(TokenObtainPairView):
    serializer_class = account_serializers.RoleBasedTokenObtainPairSerializer


class RoleListView(generics.ListAPIView):
    queryset = Group.objects.all()
    serializer_class = account_serializers.RoleResponseSerializer
    permission_classes = [permissions.CanViewRoles]


class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_active=True, is_superuser=False)
    serializer_class = account_serializers.UserResponseSerializer
    http_method_names = ["get", "post", "delete", "head", "options"]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return account_serializers.UserResponseSerializer
        elif self.action == "create":
            return account_serializers.UserRequestSerializer
        elif self.action == "assign_role":
            return account_serializers.UserRoleAssignmentSerializer
        return account_serializers.UserResponseSerializer

    def perform_create(self, serializer):
        account_service = AccountService(User, Group)
        user = account_service.create_user(
            username=serializer.validated_data["username"],
            password=serializer.validated_data["password"],
        )
        serializer.instance = user

    def perform_destroy(self, instance):
        account_service = AccountService(User, Group)
        account_service.delete_user(
            user_id=instance.id, current_user_id=self.request.user.id
        )

    @action(detail=True, methods=["post"], url_path="assign-role")
    def assign_role(self, request, pk=None):
        serializer = account_serializers.UserRoleAssignmentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        role_id = serializer.validated_data["role_id"]
        account_service = AccountService(User, Group)
        user = account_service.assign_role(
            user_id=pk, role_id=role_id, current_user_id=request.user.id
        )
        response_serializer = account_serializers.UserResponseSerializer(user)
        return Response(response_serializer.data)

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            permission_classes = [permissions.CanViewUsers]
        elif self.action in [
            "create",
            "destroy",
            "assign_role",
        ]:
            permission_classes = [permissions.CanManageUsers]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]
