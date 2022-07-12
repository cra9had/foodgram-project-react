from rest_framework import permissions


class UserOrAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            or request.user.is_staff
        )


class AuthorizedOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
        )


class AdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated
                    or request.user.is_superuser)
                )

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated
                    or request.user.is_superuser)
                )


class AuthorAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated


    def has_object_permission(self, request, view, obj):
        return (
            obj == request.user
            or request.user.is_authenticated
            and (
                request.user.is_staff
                or request.user.is_superuser
            )
        )
