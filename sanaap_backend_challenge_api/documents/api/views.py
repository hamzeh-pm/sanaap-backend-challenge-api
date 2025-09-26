from rest_framework import viewsets
from rest_framework.response import Response

from sanaap_backend_challenge_api.documents import permissions
from sanaap_backend_challenge_api.documents.api import serializers
from sanaap_backend_challenge_api.documents.models import Document
from sanaap_backend_challenge_api.documents.services import DocumentService
from rest_framework import filters
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
import os
import mimetypes
from django.http.response import FileResponse


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = serializers.DocumentResponseSerializer

    http_method_names = ["get", "post", "patch", "delete", "head", "options"]

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title"]
    ordering_fields = ["uploaded_at", "title"]
    ordering = ["-uploaded_at"]

    def get_serializer_class(self):
        if self.action == "create":
            return serializers.DocumentRequestSerializer
        elif self.action in ["partial_update"]:
            return serializers.DocumentUpdateRequestSerializer
        return serializers.DocumentResponseSerializer

    def perform_create(self, serializer):
        service = DocumentService(Document)
        document = service.create_document(
            title=serializer.validated_data["title"],
            content=serializer.validated_data["content"],
        )
        serializers.instance = document

    def perform_update(self, serializer):
        service = DocumentService(Document)
        document = service.update_document(
            document_id=serializer.instance.pk, title=serializer.validated_data["title"]
        )
        serializer.instance = document

    def perform_destroy(self, instance):
        service = DocumentService(Document)
        service.delete_document(document_id=instance.id)

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update"]:
            permission_classes = [permissions.CanAddUpdateDocument]
        elif self.action in ["list", "retrieve"]:
            permission_classes = [permissions.CanViewDocument]
        elif self.action in ["destroy"]:
            permission_classes = [permissions.CanDeleteDocument]
        return [permission() for permission in permission_classes]


class SecureDocumentView(APIView):
    permission_classes = [permissions.CanViewDocument]

    def get(self, request, document_id):
        document = get_object_or_404(Document, pk=document_id)
        file_path = document.content.path
        if not os.path.exists(file_path):
            return Response({"detail": "File not found."}, status=404)

        mime_type, _ = mimetypes.guess_type(file_path)
        response = FileResponse(
            open(file_path, "rb"), content_type=mime_type, as_attachment=False
        )
        response["Content-Disposition"] = f'inline; filename="{document.title}"'
        response["X-Content-Type-Options"] = "nosniff"
        return response
