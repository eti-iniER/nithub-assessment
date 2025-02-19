from rest_framework.throttling import BaseThrottle


class UserCreateThrottle(BaseThrottle):
    """
    Throttles the number of user creation requests that can be made in a given time period.
    """

    scope = "user_create"

    def allow_request(self, request, view):
        if request.user and request.user.is_staff:
            return True
        return super().allow_request(request, view)


class OrderCreateThrottle(BaseThrottle):
    """
    Throttles the number of orders that can be made in a given time period.
    """

    scope = "order_create"

    def allow_request(self, request, view):
        if request.user and request.user.is_staff:
            return True
        return super().allow_request(request, view)
