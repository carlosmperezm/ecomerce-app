""" This file contains all the tests for the users app"""

from typing import override, Any

from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from users.models import User, Address

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

        self._admin_user: User

        # URLS
        self.login_url: str = reverse("login")
        self.address_list_url: str = reverse("address-list")
        self.signup_url: str = reverse("signup")
        self.user_list_url: str = reverse("user-list")

        return super().setUp()

    @override
    def tearDown(self) -> None:
        self.client.logout()
        self.client.credentials()
        return super().tearDown()

    def user_detail_url(self, pk: int) -> str:
        """Return the user detail url"""
        return reverse("user-detail", args=[pk])

    def address_detail_url(self, pk: int) -> str:
        """Return the address detail url"""
        return reverse("address-detail", args=[pk])

    def create_user_admin(self, user: dict[str, Any]) -> User:
        """Create an admin user"""
        self._admin_user = User.objects.create_superuser(**user)
        Token.objects.create(user=self._admin_user)
        return self._admin_user

    def get_tokens(self, quantity: int) -> dict[str, str]:
        """
        Login many users and return a dictionary with the tokens.

        The users are testuser1, testuser2... and so on until the quantity is reached.

        Always sign each user up before log them in to get the token

        It doesn't matter if the user is already signed up, the method will log them in anyway
        """

        tokens: dict[str, str] = {}

        for index, user in enumerate(User.objects.all()):
            if index == quantity:
                break
            tokens.setdefault(user.username, Token.objects.get(user=user).key)

        return tokens

    def create_users(self, quantity: int) -> None:
        """
        Create many users base on the quantity
        """
        user: User
        for i in range(1, quantity + 1):
            user = User.objects.create_user(
                username=USERNAME + str(i),
                email=str(i) + EMAIL,
                password=PASSWORD,
            )
            Token.objects.get_or_create(user=user)

    def create_address(self, quantity: int) -> None:
        """
        Create many addresses base on the quantity
        each address is associated with a user in the same order
        ex: testuser1 -> testaddress1, testuser2 -> testaddress2...
        and so on until the quantity is reached
        """

        for i in range(1, quantity + 1):
            Address.objects.create(
                street="teststreet" + str(i),
                city="testcity" + str(i),
                state="CA",
                zip_code="l5859",
                number="testnumber" + str(i),
                user=User.objects.get(pk=i),
            )
