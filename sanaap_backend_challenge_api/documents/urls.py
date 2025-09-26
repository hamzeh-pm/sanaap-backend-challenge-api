from sanaap_backend_challenge_api.documents.api import views
from rest_framework.routers import DefaultRouter
from django.urls import path

router = DefaultRouter()

app_name = "documents"

router.register("documents", views.DocumentViewSet, basename="document")

urlpatterns = [
    path(
        "documents/secure/<int:document_id>/",
        views.SecureDocumentView.as_view(),
        name="secure_document",
    )
]
urlpatterns += router.urls
