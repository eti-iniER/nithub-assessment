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
        self.permission_classes = [IsAuthenticated]

        if self.action in ["create", "update", "partial_update", "destroy"]:
            self.permission_classes = [IsAuthenticated, IsAdminUser]
        elif self.action in ["list", "retrieve"]:
            self.permission_classes = [AllowAny]

        return super().get_permissions()


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
            self.permission_classes = [AllowAny]

        if self.action == "retrieve":
            self.permission_classes = [IsAuthenticated, IsOwner | IsAdminUser]

        self.permission_classes = [IsAuthenticated, IsAdminUser]

        return super().get_permissions()
