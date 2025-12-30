import uuid

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
from django.db import models


class MyCustomUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)

        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, first_name=None, last_name=None):
        user: User = self.create_user(
            email=email,
            password=password,
        )

        user.is_admin = True
        user.is_staff = True
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name

        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    id = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        primary_key=True,
        editable=False,
    )
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_custom = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    photo = models.ImageField(upload_to="users/", default="images/users/default.avif")
    email_notifications = models.BooleanField(default=False)

    objects = MyCustomUserManager()
    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"

    def __str__(self) -> str:
        return self.email

    def has_perm(self, perm, obj=None) -> bool:
        return True

    def has_module_perms(self, app_label) -> bool:
        return True

    def get_full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()

    def is_superuser(self) -> bool:
        return self.is_admin
