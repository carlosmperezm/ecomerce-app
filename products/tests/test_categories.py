"""Test for Categories"""

from rest_framework.response import Response
from rest_framework import status

from products.tests.test_setup import BaseTestCaseSetUp


class CategoryTest(BaseTestCaseSetUp):
    """Test Class to all the test to"""

    def test_get_categories_list_with_categories_created(self) -> None:
        """Test if a get petition to this url retorn a list of all the categories"""
        categories_to_create: int = 8
        self._create_categories(categories_to_create)
        response: Response = self.client.get(self.categories_list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), categories_to_create)

    def test_get_categories_list_with_no_categories(self) -> None:
        """Test if the api send a 404 error code if there's any categories"""
        response: Response = self.client.get(self.categories_list_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            str(response.data.get("detail")), "No Category matches the given query."
        )

    def test_category_creation(self) -> None:
        """Test if a category could be created as a Post request"""
        response: Response = self.client.post(
            self.categories_list_url, self.category_data
        )
        response.data.pop("id")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, self.category_data)

    def test_category_creation_with_wrong_data(self) -> None:
        """Test if a category could be created as a
        Post request with a wrong data"""

        # Wrong column name
        response: Response = self.client.post(
            self.categories_list_url, {"wrong_key": "underwears"}
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotEqual(response.data, self.category_data)
