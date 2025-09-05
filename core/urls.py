from django.urls import path, include
from core import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register("admin", views.AdminUserManagementView, "admin")

urlpatterns = [
    path("", include(router.urls)),
    path("welcome", views.WelcomeMessage.as_view()),
    path("signup", views.SignupView.as_view()),
    path("login", views.LoginView.as_view()),
    path("profile", views.ProfileView.as_view()),
]
