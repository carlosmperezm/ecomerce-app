from rest_framework.response import Response
from rest_framework import status

from products.tests.test_setup import BaseTestCaseSetUp


class ProductCreationTest(BaseTestCaseSetUp):
    """Test class to all the test for products list and creation"""

    # TODO

    def test_get_product_list_with_products_created(self) -> None:
        """Test if the api return all the products corretcly"""
        raise NotImplementedError()

    def test_get_product_list_with_no_products(self) -> None:
        """Test if the api return a 404 error if there is no products"""
        raise NotImplementedError()

    def test_create_product(self) -> None:
        """Test if the api creates a product correctly"""
        raise NotImplementedError()

    def test_create_product_with_wrong_data(self) -> None:
        """Test if the api does not allow to create new products with wrong values"""
        raise NotImplementedError()

    def test_get_product_by_id(self) -> None:
        """Test if a product can be retreived by id"""
        raise NotImplementedError()

    def test_get_product_by_wrong_id(self, pk: int) -> None:
        """Test if send 404 error if there no product with the id"""
        raise NotImplementedError()

    def test_delete_product_by_id(self, pk: int) -> None:
        """Test if a product can be deleted by id"""
        raise NotImplementedError()

    def test_delete_product_by_wrong_id(self, pk: int) -> None:
        """Test if send a 404 error trying to delete a product by id"""
        raise NotImplementedError()

    def test_update_product_by_id(self, pk: int) -> None:
        """Test if a product can be update by id"""
        raise NotImplementedError()

    def test_update_product_by_wrong_id(self, pk: int) -> None:
        """Test if send a 404 error trying to update a product by id"""
        raise NotImplementedError()

    def test_update_product_with_wrong_data(self) -> None:
        """Test if the api does not allow to update new products with wrong values"""
        raise NotImplementedError()
