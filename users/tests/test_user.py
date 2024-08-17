"""Test for the user Model"""

import json
from typing import override
from django.urls import reverse
from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

from users.tests.base import BaseTest
from users.models import User


class SignUpTest(BaseTest):
    """Test class if the user can sign up"""

    def test_signup(self) -> None:
        """sign up the user"""
        response: Response = self.client.post(self.signup_url, self.user_data)
        # quantity: int = 5
        # self.create_address(quantity)
        # self.client.put(reverse("user-detail", args=[1]), {"address": 1})

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

        payload: dict[str, str] = {
            "username": "testuser1",
            "password": "testpassword",
            "email": "1test@test.com",
        }
        self.create_users(1)

        response: Response = self.client.post(
            self.login_url,
            payload,
        )

        user: User = User.objects.get(pk=1)
        token: Token = Token.objects.get(user=user)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("token"), token.key)
        self.assertIsNotNone(response.data)

    def test_login_invalid_data(self) -> None:
        """Check if the user no insert any data to log in.
        The porgram should respond with a 400 error code"""
        self.create_users(2)
        # self.client.post(reverse("signup"), self.user_data)
        response: Response = self.client.post(self.login_url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data.get("error"), "Username, password and email are required"
        )

    def test_login_invalid_user(self) -> None:
        """test if the user insert no valid password or no valid username
        The program should return 400 bad request"""
        self.create_users(1)
        # self.client.post(reverse("signup"), self.user_data)
        response: Response = self.client.post(
            self.login_url,
            {
                "username": "invaliduser",
                "password": "invalidpassword",
                "email": "invalidemail",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data.get("error"), "Invalid credentials")


class UserListViewTest(BaseTest):
    """Test for the user list view"""

    def test_user_list_view_as_admin(self) -> None:
        """Test if the user list view is working correctly"""
        user_quantity: int = 5
        self.create_users(user_quantity)
        self.create_user_admin(
            {
                "username": "admin",
                "email": "admin@admin.com",
                "password": "adminpassword",
            }
        )
        self.client.login(username="admin", password="adminpassword")

        response: Response = self.client.get(self.user_list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), user_quantity + 1)

    def test_user_list_view_as_no_admin(self) -> None:
        """Test if the user list view shows all users when the request's user is not an admin"""
        self.create_users(2)
        self.client.login(username="testuser1", password="testpassword")
        response: Response = self.client.get(self.user_list_url)
        self.assertEqual(
            response.data.get("detail"),
            "You do not have permission to perform this action.",
        )

    def test_user_list_view_without_login(self) -> None:
        """Test if the user list view is working correctly"""
        response: Response = self.client.get(self.user_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_list_view_invalid_auth(self) -> None:
        """Test if the user list view is working correctly"""
        self.client.credentials(HTTP_AUTHORIZATION="Token invalidtoken")
        response: Response = self.client.get(self.user_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
