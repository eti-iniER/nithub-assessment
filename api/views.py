from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from core.permissions import IsOwner
from core.models import Product
from api.serializers import *
from api.throttles import UserCreateThrottle, OrderCreateThrottle
from drf_spectacular.utils import extend_schema_view, extend_schema

# Create your views here.


class ProductViewSet(ModelViewSet):
    serializer_class = StaffProductSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Product.objects.all_except_deleted()
        return Product.objects.available()

    def get_serializer_class(self):
        user = self.request.user

        if user.is_staff:
            return StaffProductSerializer
        return ProductSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            self.permission_classes = [AllowAny]

        return super().get_permissions()


class UserViewSet(ModelViewSet):
    serializer_class = StaffUserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]

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
        elif self.action in ["retrieve", "update", "partial_update"]:
            self.permission_classes = [IsAuthenticated, IsOwner | IsAdminUser]

        return super().get_permissions()


@extend_schema_view(
    create=extend_schema(request=CreateOrderSerializer),
)
class OrderViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Order.objects.all()

    def get_throttles(self):
        if self.action == "create":
            return [OrderCreateThrottle()]
        return super().get_throttles()

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Order.objects.all()
        return Order.objects.for_user(user)

    def get_serializer_class(self):
        user = self.request.user

        if user.is_staff:
            return StaffOrderSerializer
        return OrderSerializer

    def get_permissions(self):
        if self.action in ["create", "list", "retrieve"]:
            self.permission_classes = [IsAuthenticated]

        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
