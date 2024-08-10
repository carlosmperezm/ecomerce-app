"""Test module for the products app"""

from typing import Any

from rest_framework.response import Response
from rest_framework import status

from products.tests.test_setup import BaseTestCaseSetUp


class ProductCreationTest(BaseTestCaseSetUp):
    """Test class to all the test for products list and creation"""

    def test_get_product_list_with_products_created(self) -> None:
        """Test if the api return all the products corretcly"""
        self._create_products(6)
        response: Response = self.client.get(self.products_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 6)

    def test_get_product_list_with_no_products(self) -> None:
        """Test if the api return a 404 error if there is no products"""
        response: Response = self.client.get(self.products_list_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            str(response.data["detail"]), "No Product matches the given query."
        )

    def test_create_product(self) -> None:
        """Test if the api creates a product correctly"""
        self._create_categories(5)
        response: Response = self.client.post(self.products_list_url, self.product_data)
        response.data = self.clean_product_data(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, self.product_data)

    def test_create_product_with_wrong_data(self) -> None:
        """Test if the api does not allow to create new products with wrong values"""
        self._create_categories(3)
        column_to_change: str = "price"
        product: dict[str, Any] = {
            "name": "shorts",
            "price": 20,
            "quantity_in_stock": 50,
            "category": "no existing category",
        }

        response: Response = self.client.post(self.products_list_url, product)
        self.assertEqual(response.data.get("detail").code, "not_found")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        product["category"] = "category1"
        product[column_to_change] = "twenty"
        response = self.client.post(self.products_list_url, product)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get(column_to_change)[0].code, "invalid")

    def test_get_product_by_id(self) -> None:
        """Test if a product can be retreived by id"""
        self._create_products(6)
        response: Response = self.client.get(self.product_detail_url(2))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("id"), 2)

    def test_get_product_by_wrong_id(self) -> None:
        """Test if send 404 error if there no product with the id"""
        self._create_products(6)
        response: Response = self.client.get(self.product_detail_url(10))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data.get("detail").code, "not_found")

    def test_delete_product_by_id(self) -> None:
        """Test if a product can be deleted by id"""
        self._create_products(5)
        response: Response = self.client.delete(self.product_detail_url(3))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data, None)

    def test_delete_product_by_wrong_id(self) -> None:
        """Test if send a 404 error trying to delete a product by id"""
        self._create_products(3)
        response: Response = self.client.delete(self.product_detail_url(4))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data.get("detail").code, "not_found")

    def test_update_product_by_id(self) -> None:
        """Test if a product can be update by id"""
        self._create_products(5)
        new_product_data: dict[str, Any] = {
            "name": "new product",
            "price": 20,
            "quantity_in_stock": 50,
            "category": "category1",
            "description": "This is a description",
        }
        response: Response = self.client.put(
            self.product_detail_url(2), new_product_data
        )
        response.data = self.clean_product_data(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, new_product_data)

    def test_update_product_by_wrong_id(self) -> None:
        """Test if send a 404 error trying to update a product by id"""
        self._create_products(2)

        new_product_data: dict[str, Any] = {
            "name": "new product",
            "price": 20,
            "quantity_in_stock": 50,
            "category": "category1",
            "description": "This is a description",
        }
        response: Response = self.client.put(
            self.product_detail_url(4), new_product_data
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data.get("detail").code, "not_found")

    def test_update_product_with_wrong_data(self) -> None:
        """Test if the api does not allow to update new products with wrong values"""

        self._create_products(4)
        column_to_change: str = "quantity_in_stock"

        new_product_data: dict[str, Any] = {
            "name": "new product",
            "price": 20,
            "quantity_in_stock": "fifty",
            "category": "category1",
            "description": "This is a description",
        }
        response: Response = self.client.put(
            self.product_detail_url(4), new_product_data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get(column_to_change)[0].code, "invalid")
