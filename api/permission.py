from rest_framework.permissions import BasePermission
from rest_framework import permissions

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.METHOD in permissions.SAFE_METHODS:\
            return True
        return obj.user == request.user