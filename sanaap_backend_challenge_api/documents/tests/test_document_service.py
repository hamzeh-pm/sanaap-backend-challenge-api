from sanaap_backend_challenge_api.documents.services import DocumentService
from sanaap_backend_challenge_api.documents.models import Document


def test_create_document_success(db, fake_image):
    document_service = DocumentService(Document)
    title = "Test Document"
    document = document_service.create_document(title, fake_image)
    assert document.title == title
    assert Document.objects.count() == 1


def test_update_document_success(db, fake_image):
    document_service = DocumentService(Document)
    original_title = "Original Title"
    updated_title = "Updated Title"
    document = document_service.create_document(original_title, fake_image)
    updated_document = document_service.update_document(document.id, updated_title)
    assert updated_document.title == updated_title
    assert Document.objects.count() == 1


def test_delete_document_success(db, fake_image):
    document_service = DocumentService(Document)
    title = "Test Document"
    document = document_service.create_document(title, fake_image)
    assert Document.objects.count() == 1
    document_service.delete_document(document.id)
    assert Document.objects.count() == 0
    assert not document.content.storage.exists(document.content.name)
