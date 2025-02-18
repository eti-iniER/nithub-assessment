from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from core.models import Product
from api.serializers import *

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

        if self.action in ["create", "update", "destroy"]:
            permissions = [IsAuthenticated, IsAdminUser]

        return [permission() for permission in permissions]
