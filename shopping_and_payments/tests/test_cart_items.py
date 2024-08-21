""" This module contains tests for adding cart items """

from random import randint
from typing import Any

from rest_framework.response import Response
from rest_framework import status

from shopping_and_payments.tests.base import BaseTestCase
from shopping_and_payments.models import ShoppingCart, CartItem

from users.models import User

from products.models import Product


class AddCartItemsTest(BaseTestCase):
    """Test that a user can add cart items"""

    def test_add_cart_items(self) -> None:
        """Test that a user can add cart items"""
        user: User = self.create_users(1)[0]

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {user.auth_token}")

        number_of_products: int = 3
        cart:ShoppingCart=ShoppingCart.objects.create(user=user)
        response: Response = None

        for product in self.create_products(number_of_products):
            response = self.client.post(self.cart_items_url(1), {"product_id": product.pk, "quantity": randint(1, 100)})

            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual( response.data.get("message"), "Products added to the cart successfully.")

        cart_items = CartItem.objects.filter(cart=cart)
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

        wrong_product_id: int = 800
        user: User = self.create_users(1)[0]
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {user.auth_token}")
        ShoppingCart.objects.create(user=user)
        response: Response = None

        for product in self.create_products(2):
            wrong_product_id += 1
            response: Response = self.client.post(self.cart_items_url(1), {"product_id": wrong_product_id, "quantity": randint(1, 100)})

            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
            self.assertEqual(
                response.data.get("error"), f"Product with id {wrong_product_id} does not exist."
            )

    def test_add_cart_items_with_invalid_quantity(self) -> None:
        """Test that a user cannot add cart items with an invalid quantity"""

        user: User = self.create_users(1)[0]
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {user.auth_token}")
        ShoppingCart.objects.create(user=user)

        for product in self.create_products(2):
            response: Response = self.client.post(self.cart_items_url(1), {"product_id": product.pk, "quantity": 'invalid_quantity'})

            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(response.data.get('quantity'), ["A valid integer is required."])

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
            response: Response = self.client.post(self.cart_items_url(1), {"product_id": product.pk, "quantity": randint(1, 100)})

            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
            self.assertEqual( response.data.get("error"), "Shopping cart does not exist.")

    def test_add_cart_items_with_no_products(self) -> None:
        """Test that a user cannot add cart items without products"""

        user: User = self.create_users(1)[0]
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {user.auth_token}")
        ShoppingCart.objects.create(user=user)

        response: Response = self.client.post(self.cart_items_url(1), {"product_id": 1, "quantity": 1})

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual( response.data.get("error"), "Product with id 1 does not exist.")


class UpdateProductsInCart(BaseTestCase):
    def test_update_products_in_cart(self) -> None:
        """Test that a user can update products in a cart"""
        user: User = self.create_users(1)[0]
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {user.auth_token}")

        products: list[Product] = self.create_products(5)
        cart: ShoppingCart = ShoppingCart.objects.create(user=user)
        cart.products.set(products, through_defaults={"quantity": 1})
        item1: CartItem = CartItem.objects.get(cart=cart, product=products[0])

        for item in CartItem.objects.all():
            print(f"{item.pk} - {item.product} - {item.quantity}")

        data: dict[str, Any] = {"new_product_id": 4, "quantity": 50}

        response: Response = self.client.put(
            self.update_products_in_cart_url(cart.pk, item1.pk), data
        )

        print("----------------------------")
        for item in CartItem.objects.all():
            item.refresh_from_db()
            print(f"{item.pk} - {item.product} - {item.quantity}")

        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data.get("message"), "Products updated in the cart successfully."
        )
