from sanaap_backend_challenge_api.documents import exceptions
from django.db import transaction


class DocumentService:
    def __init__(self, document_model):
        self.document_model = document_model

    def create_document(self, title, content):
        try:
            document = self.document_model.objects.create(title=title, content=content)
            return document
        except Exception as e:
            raise exceptions.FailedToCreateDocument() from e

    def update_document(self, document_id, title):
        try:
            document = self.document_model.objects.select_for_update().get(
                id=document_id
            )
            with transaction.atomic():
                document.title = title
                document.save()
            return document
        except self.document_model.DoesNotExist as e:
            raise exceptions.DocumentNotFound() from e
        except Exception as e:
            raise exceptions.FailedToUpdateDocument() from e

    def delete_document(self, document_id):
        try:
            with transaction.atomic():
                document = self.document_model.objects.get(id=document_id)
                file_field = document.content
                document.delete()
                self._cleanup_file(file_field)
        except self.document_model.DoesNotExist as e:
            raise exceptions.DocumentNotFound() from e
        except Exception as e:
            raise exceptions.FailedToDeleteDocument() from e

    def _cleanup_file(self, file_field):
        if file_field and file_field.storage.exists(file_field.name):
            try:
                file_field.delete(save=False)
            except Exception as e:
                raise exceptions.FileCleanupError() from e
