from rest_framework import serializers
from core.models import Product, User, Order


class StaffProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "price",
            "description",
            "available_quantity",
            "last_restocked",
            "created_at",
        )


class StaffUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "is_active",
            "is_staff",
            "created_at",
        )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "email", "created_at")


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "price",
            "description",
            "available_quantity",
        )


class StaffOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            "id",
            "user",
            "total_price",
            "created_at",
        )


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            "id",
            "total_price",
            "created_at",
        )


class CreateOrderItemSerializer(serializers.Serializer):
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        error_messages={"does_not_exist": "One or more selected products are invalid."},
    )
    quantity = serializers.IntegerField(min_value=1)


class CreateOrderSerializer(serializers.Serializer):
    items = CreateOrderItemSerializer(many=True)

    def create(self, validated_data):
        user = validated_data["user"]
        items = validated_data.pop("items")

        return Order.objects.create_order(user, items)
