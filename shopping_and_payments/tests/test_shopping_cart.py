""" This module contains tests for the shopping cart creation endpoint """

from typing import Any

from random import randint

from rest_framework import status
from rest_framework.response import Response

from shopping_and_payments.tests.base import BaseTestCase

from users.models import User


class ShoppingCartCreationTest(BaseTestCase):
    """Test that a user can create a shopping cart"""

    def test_create_shopping_cart(self) -> None:
        """Test that a user can create a shopping cart"""
        user: User = self.create_users(1)[0]

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {user.auth_token}")

        response = self.client.post(self.create_shopping_cart_url)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # self.assertEqual(len(response.data.get("products")), number_of_products)

    def test_create_shopping_cart_unauthorized(self) -> None:
        """Test that a user can create a shopping cart"""
        number_of_products: int = 3
        self.create_products(number_of_products)

        data: dict[str, Any] = {
            "products": list(range(1, number_of_products + 1)),
            "quantity": 1,
        }

        response = self.client.post(self.create_shopping_cart_url, data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data.get("detail"), "Authentication credentials were not provided."
        )
        self.assertEqual(response.data.get("detail").code, "not_authenticated")


class ShoppingCartGetTest(BaseTestCase):
    """Test that a user can get a shopping cart"""

    def test_get_cart(self) -> None:
        """Test that a user can get a shopping cart"""

        self.create_shopping_carts(2)

        number_of_user: int = 1
        user: User = self.create_users(5)[number_of_user - 1]

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {user.auth_token}")

        response: Response = self.client.get(self.shopping_cart_url(number_of_user))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data)
        self.assertEqual(response.data.get("user"), number_of_user)

    def test_get_cart_not_found(self) -> None:
        """Test that a user can get a shopping cart"""

        number_of_user: int = 2
        user: User = self.create_users(5)[number_of_user - 1]

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {user.auth_token}")

        response: Response = self.client.get(self.shopping_cart_url(number_of_user))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data.get("detail").code, "not_found")
        self.assertEqual(
            response.data.get("detail"), "No ShoppingCart matches the given query."
        )

    def test_get_cart_unauthorized(self) -> None:
        """Test that a user can get a shopping cart"""

        response: Response = self.client.get(self.shopping_cart_url(1))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data.get("detail"), "Authentication credentials were not provided."
        )
        self.assertEqual(response.data.get("detail").code, "not_authenticated")

    def test_get_cart_with_user_with_no_cart(self) -> None:
        """Test that a user can get a shopping cart when has no cart"""

        user_number: int = 3
        self.create_shopping_carts(2)
        user: User = self.create_users(3)[user_number - 1]

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {user.auth_token}")

        response: Response = self.client.get(self.shopping_cart_url(user_number))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data.get("detail").code, "not_found")
        self.assertEqual(
            response.data.get("detail"), "No ShoppingCart matches the given query."
        )

    def test_get_cart_with_user_who_is_not_owner(self) -> None:
        """Test that a user can get a shopping cart when cart does not belong to user"""

        self.create_shopping_carts(2)
        # We access the position 0 to get the first user
        user: User = self.create_users(3)[0]

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {user.auth_token}")

        # We try to get the cart of the user 2 but we are logged in as user 1
        response: Response = self.client.get(self.shopping_cart_url(2))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data.get("error"), "You are not allowed to access this cart."
        )

    def test_get_cart_with_user_who_is_not_owner_but_is_staff(self) -> None:
        """Test that a user can get a shopping cart when cart does not belong to user"""

        self.create_shopping_carts(4)
        # We access the position 0 to get the first user
        user: User = self.create_users(3)[0]
        user.is_staff = True
        user.save()

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {user.auth_token}")

        # We try to get the cart of the user 2 but we are logged in as user 1
        response: Response = self.client.get(self.shopping_cart_url(4))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data)
        print(response.data)
