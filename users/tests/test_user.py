"""Test for the user Model"""

from django.urls import reverse
from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

from users.tests.base import BaseTest
from users.models import User


class SigUpTest(BaseTest):
    """Test class if the user can sign up"""

    def test_signup(self) -> None:
        """sign up the user"""
        response: Response = self.client.post(self.signup_url, self.user_data)
        self.create_address(4)
        self.client.put(reverse("user-detail", args=[1]), {"address": 1})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("username"), self.user_data.get("username"))
        self.assertEqual(response.data.get("email"), self.user_data.get("email"))
        self.assertEqual(
            response.data.get("phone_number"), self.user_data.get("phone_number")
        )

    def test_signup_invalid_data(self) -> None:
        """test if the user insert not data the api responds with a 400 error code"""
        response: Response = self.client.post(self.signup_url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginTest(BaseTest):
    """class for login tests"""

    def test_login(self) -> None:
        """test if the user has logged correctly"""
        self.client.post(reverse("signup"), self.user_data)
        response: Response = self.client.post(self.login_url, self.user_data)
        user: User = User.objects.get(username=self.user_data.get("username"))
        token: Token = get_object_or_404(Token, user=user)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("token"), token.key)

    def test_login_invalid_data(self) -> None:
        """Check if the user no insert any data to log in.
        The porgram should respond with a 400 error code"""
        self.client.post(reverse("signup"), self.user_data)
        response: Response = self.client.post(self.login_url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsNone(response.data)

    def test_login_invalid_user(self) -> None:
        """test if the user insert no valid password or no valid username
        The program should return 400 bad request"""
        self.client.post(reverse("signup"), self.user_data)
        response: Response = self.client.post(
            self.login_url, {"username": "invaliduser", "password": "invalidpassword"}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsNone(response.data)


class UserCreateAddressTest(BaseTest):
    """Test for user address creation"""

    def test_user_create_address(self) -> None:
        """test if and address can be created"""
        token: str = self.login()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        response: Response = self.client.post(
            self.create_address_url, self.address_data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
