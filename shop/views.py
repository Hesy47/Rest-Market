from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from shop import serializers, models
from drf_spectacular.utils import extend_schema


@extend_schema(tags=["shop"])
class UserProductViewSet(ReadOnlyModelViewSet):
    serializer_class = serializers.UserProductsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            models.Product.objects.filter(owner=self.request.user)
            .select_related("owner")
            .select_related("category")
            .all()
        )
