from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class RoleBasedTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add Roles claims
        token["roles"] = list(user.groups.values_list("name", flat=True))

        return token


class RoleResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["id", "name"]


class UserResponseSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "role"]

    def get_role(self, obj):
        role = obj.groups.first()
        if role:
            return role.name


class UserRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "password",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "groups": {"write_only": True},
        }
