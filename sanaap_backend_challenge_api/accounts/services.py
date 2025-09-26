from sanaap_backend_challenge_api.accounts import exceptions


class AccountService:
    def __init__(self, user_model, group_model):
        self.user_model = user_model
        self.group_model = group_model

    def create_user(self, username, password):
        # check if the role exists
        if self.user_model.objects.filter(username=username).exists():
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
                raise exceptions.OwnerDeletionException()

            user.is_active = False
            user.save()
        except self.user_model.DoesNotExist:
            raise exceptions.UserDoesNotExistException()
