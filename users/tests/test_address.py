"""Test module for address creation and detail"""

from rest_framework.response import Response
from rest_framework import status

from users.tests.base import BaseTest


class AddressCreationTest(BaseTest):
    """class for address creation tests"""

    def test_address_creation(self) -> None:
        """Test if the address is created"""

        self.create_users(1)
        self.client.login(
            username="testuser1",
            password="testpassword",
        )

        response: Response = self.client.post(self.address_list_url, self.address_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("street"), self.address_data.get("street"))
        self.assertEqual(response.data.get("city"), self.address_data.get("city"))
        self.assertEqual(response.data.get("state"), self.address_data.get("state"))
        self.assertEqual(
            response.data.get("zip_code"), self.address_data.get("zip_code")
        )
        self.assertEqual(response.data.get("number"), self.address_data.get("number"))

    def test_address_creation_with_no_user_authenticated(self) -> None:
        """Test if the address could be created with no user authenticated"""
        response: Response = self.client.post(self.address_list_url, self.address_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data.get("detail"), "Authentication credentials were not provided."
        )


class AddressUpdateTest(BaseTest):
    """Test class for address update"""

    data_to_update: dict[str, str] = {
        "street": "updatedstreet",
        "city": "updatedcity",
        "state": "NY",
        "zip_code": "l5859",
        "number": "updatednumber",
    }

    def test_update_address_by_associated_user(self) -> None:
        """Test if the address is updated with the user associated"""
        address_id: int = 1
        user_id: int = 1
        self.create_users(quantity=2)
        self.create_address(quantity=2)

        self.client.login(
            username="testuser" + str(user_id),
            password="testpassword",
        )

        response: Response = self.client.put(
            self.address_detail_url(address_id), self.data_to_update
        )

        self.assertEqual(user_id, response.data.pop("user"))
        self.assertEqual(address_id, response.data.pop("id"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.data_to_update)

    def test_update_address_with_no_user_associated(self) -> None:
        """Test if the address is updated with no user associated"""
        self.create_users(quantity=5)
        self.create_address(quantity=4)
        self.client.login(
            username="testuser2",
            password="testpassword",
        )

        response: Response = self.client.put(
            self.address_detail_url(pk=3), self.data_to_update
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data.get("error"),
            "You do not have permission to perform this action.",
        )

    def test_update_address_with_wrong_id(self) -> None:
        """Test if the address cannot be updated with wrong address id"""
        self.create_users(quantity=5)
        self.create_address(quantity=3)
        self.client.login(
            username="testuser2",
            password="testpassword",
        )

        response: Response = self.client.put(
            self.address_detail_url(4), self.data_to_update
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data.get("detail"), "No Address matches the given query."
        )

    def test_update_address_with_no_user_authenticated(self) -> None:
        """Test if the address cannot be updated with no user authenticated"""
        self.create_users(quantity=5)
        self.create_address(quantity=3)

        response: Response = self.client.put(
            self.address_detail_url(1), self.data_to_update
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data.get("detail"), "Authentication credentials were not provided."
        )

    def test_update_address_by_admin(self) -> None:
        """Test if any address is updated by admin"""
        self.create_users(quantity=5)
        self.create_address(quantity=3)
        self.create_user_admin(
            {"username": "admin", "email": "admin@admin.com", "password": "admin"}
        )
        self.client.login(
            username="admin",
            password="admin",
        )

        response: Response = self.client.put(
            self.address_detail_url(1), self.data_to_update
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(1, response.data.pop("id"))
        self.assertEqual(1, response.data.pop("user"))
        self.assertEqual(response.data, self.data_to_update)
        self.assertEqual(response.data, self.data_to_update)

        response = self.client.put(self.address_detail_url(3), self.data_to_update)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(3, response.data.pop("id"))
        self.assertEqual(3, response.data.pop("user"))
        self.assertEqual(response.data, self.data_to_update)
        self.assertEqual(response.data, self.data_to_update)


class AddressDeletionTest(BaseTest):
    """Test class for address deletion"""

    def test_delete_address_by_associated_user(self) -> None:
        """Test if the address is deleted with the user associated"""
        self.create_users(2)
        self.create_address(2)

        self.client.login(
            username="testuser1",
            password="testpassword",
        )

        response: Response = self.client.delete(self.address_detail_url(1))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("message"), "Address deleted successfully")

    def test_delete_address_with_no_user_associated(self) -> None:
        """Test if the address is deleted with no user associated"""
        self.create_users(3)
        self.create_address(3)
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.get_tokens(4).get("testuser2", "")
        )

        response: Response = self.client.delete(self.address_detail_url(1))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data.get("error"),
            "You do not have permission to perform this action.",
        )

    def test_delete_address_with_wrong_id(self) -> None:
        """Test if the address is deleted with wrong address id"""
        self.create_users(3)
        self.create_address(3)
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.get_tokens(5).get("testuser2", "")
        )
        response: Response = self.client.delete(self.address_detail_url(4))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data.get("detail"), "No Address matches the given query."
        )

    def test_delete_address_with_no_user_authenticated(self) -> None:
        """Test if the address is deleted with no user authenticated"""
        self.create_users(3)
        self.create_address(3)

        response: Response = self.client.delete(self.address_detail_url(1))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data.get("detail"), "Authentication credentials were not provided."
        )

    def test_delete_address_by_admin(self) -> None:
        """Test if any address is deleted by admin"""
        self.create_users(3)
        self.create_user_admin(
            {"username": "admin", "email": "admin@admin.com", "password": "admin"}
        )
        self.create_address(3)
        self.client.login(
            username="admin",
            password="admin",
        )
        response: Response = self.client.delete(self.address_detail_url(1))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("message"), "Address deleted successfully")

        response = self.client.delete(self.address_detail_url(2))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("message"), "Address deleted successfully")


class AddressGetTest(BaseTest):
    """Test class for addres information"""

    def test_get_address_detail_with_regular_user_associed_with_that_address(
        self,
    ) -> None:
        """Test if addres detail can corretcly be retreived
        when the user is associated with that address"""

        self.create_users(3)
        self.client.login(
            username="testuser1",
            password="testpassword",
        )
        self.create_address(2)

        address_id: int = 1

        response: Response = self.client.get(self.address_detail_url(address_id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("street"), "teststreet" + str(address_id))
        self.assertEqual(response.data.get("city"), "testcity" + str(address_id))
        self.assertEqual(response.data.get("state"), "CA")
        self.assertEqual(response.data.get("zip_code"), "l5859")
        self.assertEqual(response.data.get("number"), "testnumber" + str(address_id))

    def test_get_address_with_no_user_associated(self) -> None:
        """Test if addres detail view throws 403 error when
        no user is associated with that address"""
        self.create_users(3)
        self.create_address(3)
        self.client.login(
            username="testuser2",
            password="testpassword",
        )
        address_id: int = 3
        response: Response = self.client.get(self.address_detail_url(address_id))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data.get("error"),
            "You do not have permission to perform this action.",
        )

    def test_get_address_with_admin(self) -> None:
        """Test if address detail can be retrieved by admin even
        if the user is not associated with that address"""
        self.create_users(3)
        self.create_user_admin(
            {"username": "admin", "email": "admin@admin.com", "password": "admin"}
        )
        self.create_address(3)
        self.client.login(
            username="admin",
            password="admin",
        )
        address_id: int = 3
        response: Response = self.client.get(self.address_detail_url(address_id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("street"), "teststreet" + str(address_id))
        self.assertEqual(response.data.get("city"), "testcity" + str(address_id))
        self.assertEqual(response.data.get("state"), "CA")
        self.assertEqual(response.data.get("zip_code"), "l5859")
        self.assertEqual(response.data.get("number"), "testnumber" + str(address_id))

        address_id = 1
        response = self.client.get(self.address_detail_url(address_id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("street"), "teststreet" + str(address_id))
        self.assertEqual(response.data.get("city"), "testcity" + str(address_id))
        self.assertEqual(response.data.get("state"), "CA")
        self.assertEqual(response.data.get("zip_code"), "l5859")
        self.assertEqual(response.data.get("number"), "testnumber" + str(address_id))

    def test_get_address_with_wrong_id(self) -> None:
        """Test if address detail view throws 404 error when wrong address id is provided"""
        self.create_users(3)
        self.create_address(3)
        self.client.login(
            username="testuser2",
            password="testpassword",
        )
        address_id: int = 4
        response: Response = self.client.get(self.address_detail_url(address_id))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data.get("detail"), "No Address matches the given query."
        )

    def test_get_address_with_no_user_authenticated(self) -> None:
        """Test if address detail view throws 401 error when no user is authenticated"""
        self.create_users(3)
        self.create_address(3)
        response: Response = self.client.get(self.address_detail_url(1))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data.get("detail"), "Authentication credentials were not provided."
        )

    def test_get_all_addresses_with_regular_user(self) -> None:
        """Test if all addresses cannot be retreived by a regular user"""
        self.create_users(3)
        self.create_address(3)
        self.client.login(
            username="testuser2",
            password="testpassword",
        )
        response: Response = self.client.get(self.address_list_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data.get("error"),
            "You do not have permission to perform this action.",
        )

    def test_get_all_addresses_with_admin(self) -> None:
        """Test if all addresses can be retreived by an admin"""
        self.create_users(5)
        self.create_user_admin(
            {"username": "admin", "email": "admin@admin.com", "password": "admin"}
        )
        self.create_address(3)
        self.client.login(
            username="admin",
            password="admin",
        )
        response: Response = self.client.get(self.address_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
