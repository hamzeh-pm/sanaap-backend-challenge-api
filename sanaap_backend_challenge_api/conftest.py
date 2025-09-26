import io
import shutil

import pytest
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from PIL import Image
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def setup_groups_and_permissions(db):
    """Create groups and permissions for testing."""
    # Create groups
    admin_group, _ = Group.objects.get_or_create(name="Admin")
    editor_group, _ = Group.objects.get_or_create(name="Editor")
    viewer_group, _ = Group.objects.get_or_create(name="Viewer")

    # Get all user and group permissions
    user_group_permissions = Permission.objects.filter(
        content_type__model__in=["user", "group"]
    )
    document_view_permission = Permission.objects.get(codename="view_document")
    document_add_permission = Permission.objects.get(codename="add_document")
    document_change_permission = Permission.objects.get(codename="change_document")
    document_delete_permission = Permission.objects.get(codename="delete_document")

    # Assign to admin group
    admin_group.permissions.set(user_group_permissions)
    admin_group.permissions.add(
        document_view_permission,
        document_add_permission,
        document_change_permission,
        document_delete_permission,
    )
    editor_group.permissions.add(
        document_view_permission, document_add_permission, document_change_permission
    )
    viewer_group.permissions.add(document_view_permission)

    return {"admin": admin_group, "editor": editor_group, "viewer": viewer_group}


@pytest.fixture
def admin_user(setup_groups_and_permissions, django_user_model):
    user = django_user_model.objects.create_user(
        username="user_admin", password="password123"
    )
    user.groups.add(setup_groups_and_permissions["admin"])
    return user


@pytest.fixture
def editor_user(setup_groups_and_permissions, django_user_model):
    user = django_user_model.objects.create_user(
        username="user_editor", password="password123"
    )
    user.groups.add(setup_groups_and_permissions["editor"])
    return user


@pytest.fixture
def viewer_user(setup_groups_and_permissions, django_user_model):
    user = django_user_model.objects.create_user(
        username="user_viewer", password="password123"
    )
    user.groups.add(setup_groups_and_permissions["viewer"])
    return user


@pytest.fixture
def temp_media_root(tmp_path):
    with override_settings(MEDIA_ROOT=tmp_path):
        yield tmp_path

    # clean up after test
    shutil.rmtree(tmp_path, ignore_errors=True)


@pytest.fixture
def fake_image(temp_media_root):
    image = Image.new("RGB", (100, 100), color="red")
    image_buffer = io.BytesIO()
    image.save(image_buffer, format="JPEG")
    image_buffer.seek(0)

    return SimpleUploadedFile(
        "test_image.jpg", image_buffer.getvalue(), content_type="image/jpeg"
    )
