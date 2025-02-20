from rest_framework.permissions import BasePermission
from core.models import User


class IsOwner(BasePermission):
    """
    Allows access only to the user who owns the object.

    """

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, User):
            return obj == request.user
        return obj.user == request.user
