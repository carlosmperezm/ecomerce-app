"""Test for Products app"""

from typing import override, Any

from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from products.models import Category, Product
from users.models import User


class BaseTestCaseSetUp(APITestCase):
    """Base class to set up atributes and methods for each Test Class"""

    # URLs
    categories_list_url: str = reverse("categories-list")
    products_list_url: str = reverse("products-list")

    category_data: dict[str, str] = {"category_name": "underwears"}
    product_data: dict[str, Any] = {
        "name": "shorts",
        "price": 20,
        "quantity_in_stock": 50,
        "category": "category1",
        "description": "This is a description",
    }

    def category_detail_url(self, pk: int) -> str:
        """Return the url for the category detail view"""
        return reverse("category-detail", kwargs={"pk": pk})

    def set_headers_as_admin(self) -> None:
        """Set the headers as an admin user"""
        admin: User = User.objects.create_superuser(
            email="admin@admin.com", password="admin123", username="admin"
        )
        token: str = Token.objects.get_or_create(user=admin)[0].key

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")

    def set_headers_as_normal_user(self) -> None:
        """Set the headers as a normal user"""

        user: User = User.objects.create_user(
            email="testuser@test.com", password="test123", username="testuser"
        )

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {Token.objects.create(user=user).key}"
        )

    @override
    def setUp(self) -> None:
        return super().setUp()

    @override
    def tearDown(self) -> None:
        self.client.logout()
        self.client.credentials()
        return super().tearDown()

    def product_detail_url(self, pk: int) -> str:
        """Return the url for the product detail view"""
        return reverse("product-detail", kwargs={"pk": pk})

    def clean_product_data(self, product: dict[str, Any]) -> dict:
        """Clean the product data
        return a dict with the cleaned data
        """
        product.pop("id")
        product["category"] = product["category"]["category_name"]
        return product

    def _create_categories(self, quantity: int) -> None:
        """Create a some of categories"""
        for i in range(1, quantity + 1):
            Category.objects.create(category_name="category" + str(i))

    def _create_products(self, quantity: int) -> None:
        """Create a some of products"""
        self._create_categories(quantity)

        for i in range(1, quantity + 1):
            Product.objects.create(
                name="product" + str(i),
                category=Category.objects.get(category_name="category" + str(i)),
                quantity_in_stock=10,
                price=10.0,
            )
