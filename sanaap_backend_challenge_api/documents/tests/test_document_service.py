from sanaap_backend_challenge_api.documents.services import DocumentService
from sanaap_backend_challenge_api.documents.models import Document


def test_create_document_success(db, fake_image):
    document_service = DocumentService(Document)
    title = "Test Document"
    document = document_service.create_document(title, fake_image)
    assert document.title == title
    assert Document.objects.count() == 1
