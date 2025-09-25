def test_admin_user_can_access_role_list(admin_user, api_client):
    api_client.force_authenticate(user=admin_user)
    response = api_client.get("/api/accounts/roles/")
    assert response.status_code == 200
    assert len(response.data) == 3


def test_editor_user_cannot_access_role_list(editor_user, api_client):
    api_client.force_authenticate(user=editor_user)
    response = api_client.get("/api/accounts/roles/")
    assert response.status_code == 403


def test_viewer_user_cannot_access_role_list(viewer_user, api_client):
    api_client.force_authenticate(user=viewer_user)
    response = api_client.get("/api/accounts/roles/")
    assert response.status_code == 403
