from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from core.permissions import IsOwner
from core.models import Product, User
from api.serializers import *
from api.throttles import UserCreateThrottle

# Create your views here.


class ProductViewSet(ModelViewSet):
    serializer_class = StaffProductSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Product.objects.all()
        return Product.objects.available()

    def get_serializer_class(self):
        user = self.request.user

        if user.is_staff:
            return StaffProductSerializer
        return ProductSerializer

    def get_permissions(self):
        permissions = [IsAuthenticated]

        if self.action in ["create", "update", "partial_update", "destroy"]:
            permissions = [IsAuthenticated, IsAdminUser]
        elif self.action in ["list", "retrieve"]:
            permissions = [AllowAny]

        return [permission() for permission in permissions]


class UserViewSet(ModelViewSet):
    def get_throttles(self):
        if self.action == "create":
            return [UserCreateThrottle()]
        return super().get_throttles()

    def get_serializer_class(self):
        user = self.request.user

        if user.is_staff:
            return StaffUserSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action == "create":
            return [AllowAny()]

        if self.action == "retrieve":
            return [IsAuthenticated(), IsOwner() | IsAdminUser()]

        return [
            IsAuthenticated(),
            IsAdminUser(),
        ]
