from rest_framework import serializers
from shop import models


class UserProductsSerializer(serializers.ModelSerializer):
    """The user products endpoint serializer"""

    category = serializers.StringRelatedField()
    owner = serializers.StringRelatedField()

    class Meta:
        model = models.Product
        fields = [
            "id",
            "title",
            "description",
            "price",
            "is_available",
            "category",
            "owner",
        ]
