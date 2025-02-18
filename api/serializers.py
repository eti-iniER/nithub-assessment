from rest_framework import serializers
from core.models import Product


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
