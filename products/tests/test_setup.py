"""Test for Products app"""

from typing import override, Any

from django.urls import reverse

from rest_framework.test import APITestCase


class BaseTestCaseSetUp(APITestCase):
    """Base class to set up atributes and methods for each Test Class"""

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

    @override
    def setUp(self) -> None:
        return super().setUp()

    @override
    def tearDown(self) -> None:
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
        for i in range(quantity):
            self.client.post(
                self.categories_list_url, {"category_name": "category" + str(i)}
            )

    def _create_products(self, quantity: int) -> None:
        """Create a some of products"""
        self._create_categories(quantity)

        for i in range(quantity):
            self.client.post(
                self.products_list_url,
                {
                    "name": "product" + str(i),
                    "category": "category" + str(i),
                    "quantity_in_stock": 10,
                    "price": 10.0,
                },
            )
