from rest_framework.exceptions import APIException


class UserAlreadyExistsException(APIException):
    status_code = 400
    default_detail = "A user with the given username already exists."
    default_code = "user_already_exists"


class UserDoesNotExistException(APIException):
    status_code = 404
    default_detail = "The specified user does not exist."
    default_code = "user_does_not_exist"


class OwnerDeletionException(APIException):
    status_code = 400
    default_detail = "The owner user cannot be deleted."
    default_code = "owner_deletion_error"


class RoleDoesNotExistException(APIException):
    status_code = 400
    default_detail = "The specified role does not exist."
    default_code = "role_does_not_exist"


class InvalidRoleAssignmentException(APIException):
    status_code = 400
    default_detail = "The role assignment is invalid."
    default_code = "invalid_role_assignment"
