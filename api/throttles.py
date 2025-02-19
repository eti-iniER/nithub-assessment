from rest_framework.throttling import BaseThrottle


class UserCreateThrottle(BaseThrottle):
    scope = "user_create"

    def allow_request(self, request, view):
        # Allow unlimited requests for admins
        if request.user and request.user.is_staff:
            return True
        return super().allow_request(request, view)
