from rest_framework import permissions


class CanAddUpdateDocument(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        required_permission = ["documents.add_document", "documents.change_document"]
        return any(request.user.has_perm(perm) for perm in required_permission)


class CanViewDocument(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.has_perm(
            "documents.view_document"
        )


class CanDeleteDocument(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.has_perm(
            "documents.delete_document"
        )
