"""Test for Categories"""

from rest_framework.response import Response
from rest_framework import status

from products.tests.test_setup import BaseTestCaseSetUp
from products.models import Category


PERMISSION_ERROR: str = "You do not have permission to perform this action."


class CategoryCreationTest(BaseTestCaseSetUp):
    """Test Class to test the creation of a category"""

    def test_category_creation_as_admin_user(self) -> None:
        """Test if a category could be created as a Post request"""

        self.set_headers_as_admin()

        response: Response = self.client.post(
            self.categories_list_url, self.category_data
        )

        response.data.pop("id")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, self.category_data)

    def test_category_creation_as_normal_user(self) -> None:
        """Test if a category could be created as a Post request"""

        self.set_headers_as_normal_user()

        response: Response = self.client.post(
            self.categories_list_url, self.category_data
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data.get("error"), PERMISSION_ERROR)

    def test_category_creation_with_wrong_data(self) -> None:
        """Test if a category could be created as a
        Post request with a wrong data"""

        self.set_headers_as_admin()

        # Wrong column name
        response: Response = self.client.post(
            self.categories_list_url, {"wrong_key": "underwears"}
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotEqual(response.data, self.category_data)


class CategoryGetTest(BaseTestCaseSetUp):
    """Test Class to test the get method of the CategoryDetailView"""

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

    def test_get_categories_as_normal_user(self) -> None:
        """Test if a get petition to this url return a list of all the categories"""

        self.set_headers_as_normal_user()
        categories_to_create: int = 3
        self._create_categories(categories_to_create)

        response: Response = self.client.get(self.categories_list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), categories_to_create)

    def test_get_categoies_as_admin(self) -> None:
        """Test if a get petition to this url return a list of all the categories"""

        self.set_headers_as_admin()
        categories_to_create: int = 4
        self._create_categories(categories_to_create)

        response: Response = self.client.get(self.categories_list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), categories_to_create)

    def test_get_category_by_id_as_admin(self) -> None:
        """Test if a get petition to this url return a list of all the categories"""

        self.set_headers_as_admin()
        categories_to_create: int = 2
        self._create_categories(categories_to_create)

        category_id: int = 1
        response: Response = self.client.get(self.category_detail_url(category_id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("category_name"), "category1")

    def test_get_category_by_id_as_normal_user(self) -> None:
        """Test if a get petition to this url return a list of all the categories"""

        self.set_headers_as_normal_user()
        categories_to_create: int = 2
        self._create_categories(categories_to_create)

        category_id: int = 1
        response: Response = self.client.get(self.category_detail_url(category_id))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data.get("detail"), PERMISSION_ERROR)
        # In this case the permission error is handled by the IsAdminUser permission class
        # provided by the rest_framework.permissions module

    def test_get_category_by_id_with_no_categories_as_admin_user(self) -> None:
        """Test if a get petition to this url return a list of all the categories"""
        self.set_headers_as_admin()
        category_id: int = 1
        response: Response = self.client.get(self.category_detail_url(category_id))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data.get("detail"), "No Category matches the given query."
        )


class CategoryDeleteTest(BaseTestCaseSetUp):
    """Test Class to test the delete method of the CategoryDetailView"""

    def test_delete_category_as_admin_user(self) -> None:
        """Test if a category could be deleted as a delete request"""

        categories_quantity: int = 3
        self.set_headers_as_admin()
        self._create_categories(categories_quantity)

        response: Response = self.client.delete(self.category_detail_url(2))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data, None)
        self.assertEqual(Category.objects.count(), categories_quantity - 1)

    def test_delete_category_as_normal_user(self) -> None:
        """Test if a category could be deleted as a delete request"""

        categories_quantity: int = 2
        self.set_headers_as_normal_user()
        self._create_categories(categories_quantity)

        response: Response = self.client.delete(self.category_detail_url(1))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data.get("detail"), PERMISSION_ERROR)
        self.assertEqual(Category.objects.count(), categories_quantity)

    def test_delete_category_with_no_categories(self) -> None:
        """Test if a category could be deleted as a delete request"""

        self.set_headers_as_admin()

        response: Response = self.client.delete(self.category_detail_url(1))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data.get("detail"), "No Category matches the given query."
        )

    def test_delete_category_with_wrong_id(self) -> None:
        """Test if a category could be deleted as a delete request"""

        self.set_headers_as_admin()
        self._create_categories(2)

        response: Response = self.client.delete(self.category_detail_url(4))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data.get("detail"), "No Category matches the given query."
        )


class CategoryUpdateTest(BaseTestCaseSetUp):
    """Test Class to test the update method of the CategoryDetailView"""

    data_to_update: dict = {"category_name": "updated_category"}

    def test_update_category_as_admin_user(self) -> None:
        """Test if a category could be updated as a put request"""

        self.set_headers_as_admin()
        category_id: int = 1
        self._create_categories(1)

        response: Response = self.client.put(
            self.category_detail_url(category_id), self.data_to_update
        )

        response.data.pop("id")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.data_to_update)

    def test_update_category_as_normal_user(self) -> None:
        """Test if a category could be updated as a put request"""

        self.set_headers_as_normal_user()
        category_id: int = 1
        self._create_categories(1)

        response: Response = self.client.put(
            self.category_detail_url(category_id), self.data_to_update
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data.get("detail"), PERMISSION_ERROR)

    def test_update_category_with_no_categories(self) -> None:
        """Test if a category could be updated as a put request"""

        self.set_headers_as_admin()

        response: Response = self.client.put(
            self.category_detail_url(1), self.data_to_update
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data.get("detail"), "No Category matches the given query."
        )

    def test_update_category_with_wrong_data(self) -> None:
        """Test if a category could be updated as a put request"""

        self.set_headers_as_admin()
        self._create_categories(2)

        response: Response = self.client.put(
            self.category_detail_url(2), {"wrong_key": "underwears"}
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotEqual(response.data, self.data_to_update)

    def test_update_category_with_wrong_id(self) -> None:
        """Test if a category could be updated as a put request"""

        self.set_headers_as_admin()
        self._create_categories(2)

        response: Response = self.client.put(
            self.category_detail_url(4), self.category_data
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data.get("detail"), "No Category matches the given query."
        )

    def test_update_category_with_wrong_id_and_wrong_data(self) -> None:
        """Test if a category could be updated as a put request"""

        self.set_headers_as_admin()
        self._create_categories(1)

        response: Response = self.client.put(
            self.category_detail_url(4), {"wrong_key": "underwears"}
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data.get("detail"), "No Category matches the given query."
        )
