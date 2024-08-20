""" This module contains tests for adding cart items """

from random import randint
from typing import Any

from rest_framework.response import Response
from rest_framework import status

from shopping_and_payments.tests.base import BaseTestCase
from shopping_and_payments.models import ShoppingCart, CartItems

from users.models import User


class AddCartItemsTest(BaseTestCase):
    """Test that a user can add cart items"""

    def test_add_cart_items(self) -> None:
        """Test that a user can add cart items"""
        user: User = self.create_users(1)[0]

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {user.auth_token}")

        number_of_products: int = 3
        data: dict[str, Any] = {}

        ShoppingCart.objects.create(user=user)
        for product in self.create_products(number_of_products):
            data.setdefault(product.pk, randint(1, 100))

        response: Response = self.client.post(self.cart_items_url(1), data)

        cart = ShoppingCart.objects.get(pk=1)
        cart_items = CartItems.objects.filter(cart=cart)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data.get("message"), "Products added to the cart successfully."
        )
        self.assertEqual(cart.products.all().count(), number_of_products)
        self.assertEqual(cart_items.count(), number_of_products)

    def test_add_cart_items_with_no_auth(self) -> None:
        """Test that a user cannot add cart items without authentication"""
        number_of_products: int = 4
        data: dict[str, Any] = {}

        for product in self.create_products(number_of_products):
            data.setdefault(product.pk, randint(1, 100))

        ShoppingCart.objects.create(user=self.create_users(1)[0])
        response: Response = self.client.post(self.cart_items_url(1), data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data.get("detail"), "Authentication credentials were not provided."
        )

    def test_add_cart_items_with_no_wrong_auth(self) -> None:
        """Test that a user cannot add cart items without authentication"""
        users: list[User] = self.create_users(3)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {users[0].auth_token}")
        number_of_products: int = 4
        data: dict[str, Any] = {}

        for product in self.create_products(number_of_products):
            data.setdefault(product.pk, randint(1, 100))

        ShoppingCart.objects.create(user=users[2])
        response: Response = self.client.post(self.cart_items_url(1), data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data.get("error"),
            "You do not have permission to perform this action.",
        )

    def test_add_cart_items_with_invalid_product(self) -> None:
        """Test that a user cannot add cart items with an invalid product"""

        user: User = self.create_users(1)[0]
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {user.auth_token}")
        ShoppingCart.objects.create(user=user)
        data: dict[str, Any] = {
            "800": 1,
            "invalid_key": 1,
        }  # invalid_key is not a valid product id , 800 is not a valid product id

        for product in self.create_products(2):
            data.setdefault(product.pk, randint(1, 100))

        response: Response = self.client.post(self.cart_items_url(1), data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data.get("error"), "Product with id 800 does not exist."
        )

    def test_add_cart_items_with_invalid_quantity(self) -> None:
        """Test that a user cannot add cart items with an invalid quantity"""
        user: User = self.create_users(1)[0]
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {user.auth_token}")
        ShoppingCart.objects.create(user=user)
        data: dict[str, Any] = {}

        for product in self.create_products(2):
            data.setdefault(product.pk, "invalid_quantity {randint(1, 100)}")

        response: Response = self.client.post(self.cart_items_url(1), data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("error"), "Quantity must be an integer.")

    def test_add_cart_items_with_no_data(self) -> None:
        """Test that a user cannot add cart items without data"""
        user: User = self.create_users(1)[0]
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {user.auth_token}")
        ShoppingCart.objects.create(user=user)
        data: dict[str, Any] = {}

        response: Response = self.client.post(self.cart_items_url(1), data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("error"), "No data provided.")

    def test_add_cart_items_with_no_cart(self) -> None:
        """Test that a user cannot add cart items without a cart"""

        user: User = self.create_users(1)[0]
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {user.auth_token}")
        data: dict[str, Any] = {}

        for product in self.create_products(2):
            data.setdefault(product.pk, randint(1, 100))

        response: Response = self.client.post(self.cart_items_url(1), data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data.get("detail"), "No ShoppingCart matches the given query."
        )

    def test_add_cart_items_with_no_products(self) -> None:
        """Test that a user cannot add cart items without products"""

        user: User = self.create_users(1)[0]
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {user.auth_token}")
        ShoppingCart.objects.create(user=user)
        data: dict[str, Any] = {"1": 213, "2": 123}

        response: Response = self.client.post(self.cart_items_url(1), data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data.get("error"), "Product with id 1 does not exist."
        )
