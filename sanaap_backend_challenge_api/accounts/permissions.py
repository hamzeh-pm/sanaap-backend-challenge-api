from rest_framework import permissions


class HasRolePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        required_permission = getattr(view, "required_permission", None)
        if required_permission:
            return request.user.has_perm(required_permission)

        return False


class CanManageUsers(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        required_permission = ["auth.change_user", "auth.add_user", "auth.delete_user"]
        return any(request.user.has_perm(perm) for perm in required_permission)


class CanViewUsers(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.has_perm("auth.view_user")


class CanViewRoles(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.has_perm(
            "auth.view_group"
        )
