from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class RoleBasedTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add Roles claims
        token["roles"] = list(user.groups.values_list("name", flat=True))

        return token
