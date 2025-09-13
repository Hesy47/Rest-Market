from django.urls import path, include
from shop import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register("user-products", views.UserProductViewSet, "user-products")


urlpatterns = [
    path("", include(router.urls)),
]
