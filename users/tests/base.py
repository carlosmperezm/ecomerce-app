""" This file contains all the tests for the users app"""

from typing import override, Any

from django.urls import reverse

from rest_framework.response import Response
from rest_framework.test import APITestCase


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
            "username": "testuser",
            "email": "test@test.com",
            "password": "testpassword",
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

    def login(self) -> str:
        """Login the user and return the token key as string"""
        self.user_data = {
            "username": "testuser",
            "email": "test@test.com",
            "password": "testpassword",
        }
        self.client.post(reverse("signup"), self.user_data)
        response: Response = self.client.post(reverse("login"), self.user_data)
        return response.data.get("token")

    def create_address(self, quantity: int) -> None:
        """Create many addresses base on the quantity"""
        token: str = self.login()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        for i in range(1, quantity + 1):
            self.client.post(
                reverse("address-list"),
                {
                    "street": "teststreet" + str(i),
                    "city": "testcity" + str(i),
                    "state": "CA",
                    "zip_code": "l5859",
                    "number": "testnumber" + str(i),
                },
            )
