""" This module contains the base test case class for the shopping_and_payments app """

from typing import override

from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from shopping_and_payments.models import ShoppingCart

from products.models import Product

from users.models import User


class BaseTestCase(APITestCase):
    """Base test case class for the shopping_and_payments app"""

    @override
    def setUp(self) -> None:
        """Set up the test case"""
        # URLs
        self.order_status_url: str = reverse("order_status_create")
        self.create_shopping_cart_url: str = reverse("create_shopping_cart")
        super().setUp()

    @override
    def tearDown(self) -> None:
        """Tear down the test case"""
        self.client.logout()
        self.client.credentials()
        super().tearDown()

    def shopping_cart_url(self, pk: int) -> str:
        """Return the shopping cart URL"""
        return reverse("shopping_cart", args=[pk])

    def cart_items_url(self, pk: int) -> str:
        """Return the cart items URL"""
        return reverse("add_products_to_cart", args=[pk])

    def shopping_cart_url_detail(self, pk: int) -> str:
        """Return the shopping cart URL"""
        return reverse("shopping_cart_detail", args=[pk])

    def create_products(self, number_of_products: int) -> list[Product]:
        """Create products"""
        products: list[Product] = []
        for i in range(1, number_of_products + 1):
            products.append(
                Product.objects.create(
                    name=f"Product {i}",
                    description=f"Description {i}",
                    price=i * 10,
                    quantity_in_stock=i * 10,
                )
            )
        return products

    def create_superuser(self) -> User:
        """Create a superuser and return the token"""
        admin: User = User.objects.create_superuser(
            username="admin",
            email="admin@admin.com",
            password="admin123",
        )
        Token.objects.create(user=admin)
        return admin

    def create_users(self, number_of_users: int) -> list[User]:
        """Create a user and return the token"""
        user: User = User()
        users: list[User] = []
        for i in range(1, number_of_users + 1):
            try:
                user = User.objects.get_or_create(
                    username=f"User {i}",
                    email=f"{i}user@test.com",
                    password="test123",
                )[0]
                Token.objects.get_or_create(user=user)
                users.append(user)
            except Exception as e:
                print(f"Error creating user:{i} :{e}")
        return users

    def create_shopping_carts(self, number_of_carts: int) -> list[ShoppingCart]:
        """Create shopping carts"""
        carts: list[ShoppingCart] = []
        users: list[User] = self.create_users(number_of_carts)
        products: list[Product] = self.create_products(number_of_carts)

        for i in range(1, number_of_carts + 1):
            cart: ShoppingCart = ShoppingCart.objects.create(
                user=users[i - 1],
            )
            cart.products.set(products[:i], through_defaults={"quantity": i})
            carts.append(cart)

        return carts
