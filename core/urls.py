from django.urls import path
from core import views

urlpatterns = [
    path("welcome", views.WelcomeMessage.as_view()),
]
