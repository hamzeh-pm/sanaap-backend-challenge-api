import pytest
from django.contrib.auth.models import Group
from rest_framework.test import APIClient

from django.contrib.auth.models import Group, Permission


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

    # Assign to admin group
    admin_group.permissions.set(user_group_permissions)

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
