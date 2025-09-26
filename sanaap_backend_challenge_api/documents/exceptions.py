from rest_framework.exceptions import APIException


class FailedToCreateDocument(APIException):
    status_code = 500
    default_detail = "Failed to create document."
    default_code = "failed_to_create_document"
