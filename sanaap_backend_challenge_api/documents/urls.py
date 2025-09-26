from sanaap_backend_challenge_api.documents.api import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

app_name = "documents"

router.register("documents", views.DocumentViewSet, basename="document")

urlpatterns = router.urls
