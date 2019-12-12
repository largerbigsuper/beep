from rest_framework.permissions import BasePermission, IsAuthenticated

class IsOwerPermission(IsAuthenticated):

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'user'):
            return request.user == obj.user


class IsOwnerOrAdminPermission(IsAuthenticated):

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'user'):
            return request.user == obj.user or request.user.is_superuser

