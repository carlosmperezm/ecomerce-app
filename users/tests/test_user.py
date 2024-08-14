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
        quantity: int = 5
        self.create_address(quantity)
        self.client.put(reverse("user-detail", args=[1]), {"address": 1})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data.get("username"),
            self.user_data.get("username"),
        )
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


class UserListViewTest(BaseTest):
    """Test for the user list view"""

    def test_user_list_view(self) -> None:
        """Test if the user list view is working correctly"""
        user_quantity: int = 5
        self.client.credentials(
            HTTP_AUTHORIZATION="Token "
            + self.get_tokens(user_quantity).get("testuser1", " ")
        )

        response: Response = self.client.get(self.user_list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), user_quantity)

    def test_user_list_view_no_auth(self) -> None:
        """Test if the user list view is working correctly"""
        response: Response = self.client.get(self.user_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_list_view_invalid_auth(self) -> None:
        """Test if the user list view is working correctly"""
        self.client.credentials(HTTP_AUTHORIZATION="Token invalidtoken")
        response: Response = self.client.get(self.user_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
