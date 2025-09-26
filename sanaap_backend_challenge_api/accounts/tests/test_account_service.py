import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from sanaap_backend_challenge_api.accounts import exceptions
from sanaap_backend_challenge_api.accounts.services import AccountService

User = get_user_model()


def test_create_user_success(db):
    service = AccountService(User, Group)
    username = "newuser"
    password = "newpassword"
    user = service.create_user(username, password)
    assert user.username == username
    assert user.check_password(password)


def test_delete_user_success(db):
    service = AccountService(User, Group)
    user = User.objects.create_user(username="todelete", password="password")
    user_id = user.id
    service.delete(user_id)
    user.refresh_from_db()
    assert not user.is_active


def test_cannot_delete_owner(db):
    service = AccountService(User, Group)
    user = User.objects.create_user(username="owner", password="password")
    user_id = user.id
    with pytest.raises(Exception) as e:
        service.delete_user(user_id, current_user_id=user_id)
        assert isinstance(e.value, exceptions.OwnerDeletionException)


def test_assign_role_success(db):
    service = AccountService(User, Group)
    user = User.objects.create_user(username="roleuser", password="password")
    role = Group.objects.get(name="Editor")
    service.assign_role(user.id, role.id, current_user_id=999)  # 999 not the same user
    user.refresh_from_db()
    assert user.groups.filter(name=role.name).exists()
