from rest_framework.permissions import BasePermission, IsAuthenticated

class IsOwerPermission(IsAuthenticated):

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user