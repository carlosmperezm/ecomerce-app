"""Users app models"""

from typing import override, Any

from django.db.models import (
    Model,
    EmailField,
    CharField,
    SET_NULL,
    Manager,
    OneToOneField,
)
from django.contrib.auth.models import AbstractUser, UserManager


class Address(Model):
    """Address Model"""

    id: Any = None
    user: OneToOneField = OneToOneField(
        "User", on_delete=SET_NULL, null=True, blank=True, related_name="address"
    )
    street: CharField = CharField(max_length=100)
    city: CharField = CharField(max_length=100)
    state: CharField = CharField(max_length=100)
    zip_code: CharField = CharField(max_length=10)
    number: CharField = CharField(max_length=100)

    objects = Manager()

    @override
    def __str__(self) -> str:
        return f"{self.street},{self.city},{self.state},{self.zip_code}"


class User(AbstractUser):
    """User Model"""

    email: EmailField = EmailField(
        verbose_name="email address", unique=True, max_length=100
    )
    username: CharField = CharField(max_length=100, unique=True)
    phone_number: CharField = CharField(max_length=15, null=True, blank=True)

    objects = UserManager()

    REQUIRED_FIELDS = ["email"]

    @override
    def __str__(self) -> str:
        return str(self.email)
