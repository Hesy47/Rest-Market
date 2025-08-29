from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone


class UserManager(BaseUserManager):
    """The Django user creation system"""

    def create_user(self, email: str, username: str, password: str, **extra_fields):
        if not email:
            raise ValueError("each user must have a unique email address")

        if not username:
            raise ValueError("each user must have a unique username")

        if not password:
            raise ValueError("each user must have a password")

        email = self.normalize_email(email)
        username = username.strip()

        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(
        self, email: str, username: str, password: str, **extra_fields
    ):
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """The user database model"""

    email = models.EmailField(
        max_length=60,
        unique=True,
        error_messages={"unique": "this email address is already taken"},
    )

    username = models.CharField(
        max_length=30,
        unique=True,
        error_messages={"unique": "This username is already taken"},
    )

    phone_number = models.CharField(
        max_length=11,
        unique=True,
        error_messages={"unique": "This phone number is already taken"},
    )

    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "phone_number"]

    def __str__(self):
        return self.username

    class Meta:
        db_table = "users"
