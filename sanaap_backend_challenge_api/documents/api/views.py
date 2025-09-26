from rest_framework import viewsets
from rest_framework.response import Response

from sanaap_backend_challenge_api.documents import permissions
from sanaap_backend_challenge_api.documents.api import serializers
from sanaap_backend_challenge_api.documents.models import Document
from sanaap_backend_challenge_api.documents.services import DocumentService

from django.shortcuts import get_object_or_404


class DocumentViewSet(viewsets.ViewSet):
    def list(self, request):
        data = Document.objects.all()
        serializer = serializers.DocumentResponseSerializer(data, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        document = get_object_or_404(Document, pk=pk)
        serializer = serializers.DocumentResponseSerializer(document)
        return Response(serializer.data)

    def create(self, request):
        service = DocumentService(Document)
        serializer = serializers.DocumentRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        document = service.create_document(
            title=serializer.validated_data["title"],
            content=serializer.validated_data["content"],
        )
        response_serializer = serializers.DocumentResponseSerializer(document)
        return Response(response_serializer.data, status=201)

    def partial_update(self, request, pk=None):
        service = DocumentService(Document)
        serializer = serializers.DocumentUpdateRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        document = service.update_document(
            document_id=pk, title=serializer.validated_data["title"]
        )
        response_serializer = serializers.DocumentResponseSerializer(document)
        return Response(response_serializer.data)

    def destroy(self, request, pk=None):
        service = DocumentService(Document)
        service.delete_document(document_id=pk)
        return Response(status=204)

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update"]:
            permission_classes = [permissions.CanAddUpdateDocument]
        elif self.action in ["list", "retrieve"]:
            permission_classes = [permissions.CanViewDocument]
        elif self.action in ["destroy"]:
            permission_classes = [permissions.CanDeleteDocument]
        return [permission() for permission in permission_classes]
