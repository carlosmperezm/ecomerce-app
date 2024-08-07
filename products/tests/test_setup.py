"""Test for Products app"""

from typing import override

from django.urls import reverse

from rest_framework.test import APITestCase


class BaseTestCaseSetUp(APITestCase):
    """Base class to set up atributes and methods for each Test Class"""

    categories_list_url: str = reverse("categories-list")
    products_list_url: str = reverse("products-list")
    product_detail_url: str = reverse("product-detail", kwargs={"pk": 1})
    category_data: dict[str, str] = {"category_name": "underwears"}

    @override
    def setUp(self) -> None:
        return super().setUp()

    @override
    def tearDown(self) -> None:
        return super().tearDown()

    def _create_categories(self, quantity: int) -> int:
        """Create a some of categories
        Return the number of categories created"""
        categories_list_names: tuple[str, ...] = (
            "underwear",
            "pants",
            "men",
            "gym",
            "women",
            "shorts",
        )

        if quantity >= len(categories_list_names):
            for category_name in categories_list_names:
                self.client.post(
                    self.categories_list_url, {"category_name": category_name}
                )
            return len(categories_list_names)

        for index, category_name in enumerate(categories_list_names):
            if quantity == index:
                return quantity
            self.client.post(self.categories_list_url, {"category_name": category_name})

        return 0
