from sanaap_backend_challenge_api.accounts.services import AccountService
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()


def test_create_user_success(db):
    service = AccountService(User, Group)
    username = "newuser"
    password = "newpassword"
    user = service.create_user(username, password)
    assert user.username == username
    assert user.check_password(password)
