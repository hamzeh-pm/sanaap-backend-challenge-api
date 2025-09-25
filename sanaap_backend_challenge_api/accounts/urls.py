from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from sanaap_backend_challenge_api.accounts.api.views import (
    RoleBasedTokenObtainPairView,
    RoleListView,
)

app_name = "accounts"

urlpatterns = [
    path("token/", RoleBasedTokenObtainPairView.as_view(), name="token-obtain-pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("roles/", RoleListView.as_view(), name="role-list"),
]
