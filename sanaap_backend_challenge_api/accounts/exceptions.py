from rest_framework.exceptions import APIException


class RoleDoesNotExistException(APIException):
    status_code = 400
    default_detail = "The specified role does not exist."
    default_code = "role_does_not_exist"


class UserAlreadyExistsException(APIException):
    status_code = 400
    default_detail = "A user with the given username already exists."
    default_code = "user_already_exists"


class InvalidRoleAssignmentException(APIException):
    status_code = 400
    default_detail = "The role assignment is invalid."
    default_code = "invalid_role_assignment"
