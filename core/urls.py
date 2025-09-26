from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView
from drf_spectacular.views import SpectacularSwaggerView

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    # JWT auth
    path(
        "api/accounts/",
        include("sanaap_backend_challenge_api.accounts.urls", namespace="accounts"),
    ),
    path(
        "api/documents/",
        include("sanaap_backend_challenge_api.documents.urls", namespace="documents"),
    ),
]

# API URLS
urlpatterns += [
    path("api/schema/", SpectacularAPIView.as_view(), name="api-schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="api-schema"),
        name="api-docs",
    ),
]
