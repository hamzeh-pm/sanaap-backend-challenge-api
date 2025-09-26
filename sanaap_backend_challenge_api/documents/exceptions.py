from rest_framework.exceptions import APIException


class FailedToCreateDocument(APIException):
    status_code = 500
    default_detail = "Failed to create document."
    default_code = "failed_to_create_document"


class DocumentNotFound(APIException):
    status_code = 404
    default_detail = "Document not found."
    default_code = "document_not_found"


class FailedToUpdateDocument(APIException):
    status_code = 500
    default_detail = "Failed to update document."
    default_code = "failed_to_update_document"


class FailedToDeleteDocument(APIException):
    status_code = 500
    default_detail = "Failed to delete document."
    default_code = "failed_to_delete_document"


class FileCleanupError(APIException):
    status_code = 500
    default_detail = "Failed to clean up file."
    default_code = "file_cleanup_error"
