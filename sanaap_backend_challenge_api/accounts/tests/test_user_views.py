def test_user_list(admin_user, editor_user, api_client):
    api_client.force_authenticate(user=admin_user)
    response = api_client.get("/api/accounts/users/")
    assert response.status_code == 200
    assert len(response.data) == 2  # Excludes superuser


def test_non_admin_user_cannot_access_user_list(editor_user, api_client):
    api_client.force_authenticate(user=editor_user)
    response = api_client.get("/api/accounts/users/")
    assert response.status_code == 403


def test_user_detail(admin_user, viewer_user, api_client):
    api_client.force_authenticate(user=admin_user)
    response = api_client.get(f"/api/accounts/users/{viewer_user.id}/")
    assert response.status_code == 200
    assert response.data["username"] == viewer_user.username


def test_non_admin_user_cannot_access_user_detail(editor_user, viewer_user, api_client):
    api_client.force_authenticate(user=editor_user)
    response = api_client.get(f"/api/accounts/users/{viewer_user.id}/")
    assert response.status_code == 403
