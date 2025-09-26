from sanaap_backend_challenge_api.documents.models import Document


def test_viewer_user_can_access_document_list(viewer_user, api_client, fake_image):
    # clear existing documents
    api_client.force_authenticate(user=viewer_user)
    Document.objects.create(title="Test Document", content=fake_image)
    response = api_client.get("/api/documents/documents/")
    assert response.status_code == 200


def test_viewer_user_cannot_access_document_create(viewer_user, api_client, fake_image):
    api_client.force_authenticate(user=viewer_user)
    data = {"title": "New Document", "content": fake_image}
    response = api_client.post("/api/documents/documents/", data, format="multipart")
    assert response.status_code == 403


def test_editor_user_cannot_delete_document(editor_user, api_client, fake_image):
    document = Document.objects.create(title="Test Document", content=fake_image)
    api_client.force_authenticate(user=editor_user)
    response = api_client.delete(f"/api/documents/documents/{document.id}/")
    assert response.status_code == 403
