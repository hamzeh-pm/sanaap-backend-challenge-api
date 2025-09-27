from sanaap_backend_challenge_api.accounts import exceptions
from logging import getLogger

logger = getLogger(__name__)


class AccountService:
    def __init__(self, user_model, group_model):
        self.user_model = user_model
        self.group_model = group_model

    def create_user(self, username, password):
        # check if the role exists
        if self.user_model.objects.filter(username=username).exists():
            logger.error(
                f"Service: Account Service, Method: create_user, Error: username {username} already exists."
            )
            raise exceptions.UserAlreadyExistsException()

        user = self.user_model.objects.create_user(username=username, password=password)
        user.save()
        return user

    def delete_user(self, user_id, current_user_id):
        try:
            user = self.user_model.objects.get(
                id=user_id, is_active=True, is_superuser=False
            )

            if user.id == current_user_id:
                logger.error(
                    f"Service: Account Service, Method: delete_user, Error: user.id {user.id} cannot delete their own account."
                )
                raise exceptions.OwnerDeletionException()

            user.is_active = False
            user.save()
        except self.user_model.DoesNotExist:
            logger.error(
                f"Service: Account Service, Method: delete_user, Error: user.id {user_id} does not exist."
            )
            raise exceptions.UserDoesNotExistException()

    def assign_role(self, user_id, role_id, current_user_id):
        try:
            user = self.user_model.objects.get(
                id=user_id, is_active=True, is_superuser=False
            )

            if user.id == current_user_id:
                logger.error(
                    f"Service: Account Service, Method: assign_role, Error: user.id {user.id} cannot change their own roles."
                )
                raise exceptions.InvalidRoleAssignmentException(
                    "Users cannot change their own roles."
                )

            role = self.group_model.objects.get(id=role_id)
            user.groups.clear()  # clear existing roles this version supports single role per user
            user.groups.add(role)
            user.save()
            return user
        except self.user_model.DoesNotExist:
            logger.error(
                f"Service: Account Service, Method: assign_role, Error: user.id {user_id} does not exist."
            )
            raise exceptions.UserDoesNotExistException()
        except self.group_model.DoesNotExist:
            logger.error(
                f"Service: Account Service, Method: assign_role, Error: role.id {role_id} does not exist."
            )
            raise exceptions.RoleDoesNotExistException()
