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
