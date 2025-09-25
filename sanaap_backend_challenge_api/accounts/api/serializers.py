from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import Group
from rest_framework import serializers


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
