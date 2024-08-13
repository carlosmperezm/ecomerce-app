""" This file contains all the tests for the users app"""

from typing import override, Any

from django.urls import reverse

from rest_framework.response import Response
from rest_framework.test import APITestCase

EMAIL: str = "test@test.com"
USERNAME: str = "testuser"
PASSWORD: str = "testpassword"


class BaseTest(APITestCase):
    """Class base to set up all the pervious data and methods"""

    user_data: dict[str, str] = {}

    @override
    def setUp(self) -> None:
        self.address_data: dict[str, str] = {
            "street": "teststreet",
            "city": "testcity",
            "state": "CA",
            "zip_code": "l5859",
            "number": "testnumber",
        }

        self.user_data: dict[str, Any] = {
            "username": USERNAME,
            "email": EMAIL,
            "password": PASSWORD,
        }

        # URLS
        self.create_address_url: str = reverse("user-create-address")
        self.login_url: str = reverse("login")
        self.address_list_url: str = reverse("address-list")
        self.signup_url: str = reverse("signup")

        return super().setUp()

    def address_detail_url(self, pk: int) -> str:
        """Return the address detail url"""
        return reverse("address-detail", args=[pk])

    def get_tokens(self, quantity: int) -> dict[str, str]:
        """Login the user and return the token key as string"""
        tokens: dict[str, str] = {}
        user_data: dict[str, str] = {}

        for i in range(1, quantity + 1):
            user_data = {
                "username": USERNAME + str(i),
                "email": str(i) + EMAIL,
                "password": PASSWORD,
            }

            self.client.post(reverse("signup"), user_data)
            response: Response = self.client.post(reverse("login"), user_data)
            tokens["testuser" + str(i)] = response.data.get("token")

        return tokens

    def signup(self, quantity: int) -> list[dict[str, str]]:
        """Create many users base on the quantity"""
        users: list[dict[str, str]] = []
        for i in range(1, quantity + 1):
            user_data = {
                "username": USERNAME + str(i),
                "email": str(i) + EMAIL,
                "password": PASSWORD,
            }
            users.append(user_data)
        return users

    def create_address(self, quantity: int) -> None:
        """Create many addresses base on the quantity"""
        tokens: dict[str, str] = self.get_tokens(quantity)

        for i in range(1, quantity + 1):
            self.client.credentials(
                HTTP_AUTHORIZATION="Token " + tokens.get("testuser" + str(i), "")
            )
            self.client.post(
                reverse("address-list"),
                {
                    "street": "teststreet" + str(i),
                    "city": "testcity" + str(i),
                    "state": "CA",
                    "zip_code": "l5859",
                    "number": "testnumber" + str(i),
                    "user": i,
                },
            )
