import base64
import mimetypes
import os

import boto3
from botocore.exceptions import ClientError
from django.conf import settings
from django.http.response import FileResponse
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import filters
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from sanaap_backend_challenge_api.documents import permissions
from sanaap_backend_challenge_api.documents import tasks
from sanaap_backend_challenge_api.documents.api import serializers
from sanaap_backend_challenge_api.documents.models import Document
from sanaap_backend_challenge_api.documents.services import DocumentService
from sanaap_backend_challenge_api.utils.mixins import ViewsetAccessLogMixin
from sanaap_backend_challenge_api.utils.paginations import CustomPagination
from sanaap_backend_challenge_api.utils.schemas import TaskResponse


class DocumentViewSet(ViewsetAccessLogMixin, viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = serializers.DocumentResponseSerializer
    pagination_class = CustomPagination

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
        title = serializer.validated_data["title"]
        content = serializer.validated_data["content"]

        # i have 3 solutions here to send the file to celery task
        # 1. save the file to a shared volume between django and celery worker container (not good containers must be stateless)
        # 2. save the file into local storage like S3 (best practice in my opinion)
        # for the sake of this challenge i consider MinIO not local storage but implemented locally for testing
        # 3. encode the file to base64 and send it to celery task (not good for large files but ok for this challenge)
        content.seek(0)
        file_content = base64.b64encode(content.read()).decode("utf-8")

        task = tasks.upload_document.delay(
            title, file_content, content.name, content.content_type
        )

        serializer.instance = TaskResponse(task_id=task.id, title=title)

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

        return self._secure_serve_from_s3(document)

    def _secure_serve_from_local(self, document):
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

    def _secure_serve_from_s3(self, document):
        try:
            s3_client = boto3.client(
                "s3",
                endpoint_url=settings.AWS_S3_ENDPOINT_URL,
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=getattr(settings, "AWS_S3_REGION_NAME", "us-east-1"),
                use_ssl=getattr(settings, "AWS_S3_USE_SSL", False),
                verify=getattr(settings, "AWS_S3_VERIFY", False),
            )

            bucket_name = settings.AWS_STORAGE_BUCKET_NAME
            object_key = document.content.name

            response = s3_client.get_object(Bucket=bucket_name, Key=object_key)

            content_type = response.get("ContentType", "application/octet-stream")

            django_response = HttpResponse(
                response["Body"].read(), content_type=content_type
            )
            django_response["Content-Disposition"] = (
                f'inline; filename="{document.title}"'
            )
            django_response["X-Content-Type-Options"] = "nosniff"
            django_response["Cache-Control"] = "private, max-age=3600"

            return django_response
        except ClientError as e:
            return Response(f"Error retrieving file: {str(e)}", status=500)
        except Exception as e:
            return Response(f"Unexpected error: {str(e)}", status=500)
