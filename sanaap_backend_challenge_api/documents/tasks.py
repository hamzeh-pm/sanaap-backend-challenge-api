import base64
from logging import getLogger

from celery import shared_task
from django.core.files.base import ContentFile

from sanaap_backend_challenge_api.documents.models import Document
from sanaap_backend_challenge_api.documents.services import DocumentService

logger = getLogger(__name__)


@shared_task
def upload_document(title, file_content, original_name, content_type):
    try:
        content = base64.b64decode(file_content)
        django_file = ContentFile(content, name=original_name)
        django_file.content_type = content_type

        service = DocumentService(Document)
        document = service.create_document(title=title, content=django_file)

        logger.info(
            f"Task: upload_document, Success: Uploaded document ID {document.id}"
        )
    except Exception as e:
        logger.error(f"Task: upload_document, Error: {str(e)}")
        raise
