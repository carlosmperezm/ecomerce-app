"""Test module for address creation and detail"""

from rest_framework.response import Response
from rest_framework import status

from users.tests.base import BaseTest


class AddressCreationTest(BaseTest):
    """class for address creation tests"""

    def test_address_creation(self) -> None:
        """Test if the address is created"""
        token: str = self.get_tokens(1).get("testuser1", "")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
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
        """Test if the address is created with no user authenticated"""
        response: Response = self.client.post(self.address_list_url, self.address_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AddressUpdateTest(BaseTest):
    """Test class for address update"""

    data_to_update: dict[str, str] = {
        "street": "updatedstreet",
        "city": "updatedcity",
        "state": "NY",
        "zip_code": "l5859",
        "number": "updatednumber",
    }

    def test_update_address(self) -> None:
        """Test if the address is updated"""
        self.create_address(2)
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.get_tokens(2).get("testuser1", "")
        )
        response: Response = self.client.put(
            self.address_detail_url(1), self.data_to_update
        )
        response.data.pop("id")
        address_user: int = response.data.pop("user")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.data_to_update)
        self.assertEqual(
            address_user, 1
        )  # testuser1 created previously is the user number 1

    def test_update_address_with_no_user_associated(self) -> None:
        """Test if the address is updated with no user associated"""
        self.create_address(4)
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.get_tokens(4).get("testuser2", "")
        )
        response: Response = self.client.put(
            self.address_detail_url(3), self.data_to_update
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_address_with_wrong_id(self) -> None:
        """Test if the address is updated with wrong address id"""
        self.create_address(3)
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.get_tokens(5).get("testuser2", "")
        )
        response: Response = self.client.put(
            self.address_detail_url(4), self.data_to_update
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class AddressDeletionTest(BaseTest):
    """Test class for address deletion"""

    def test_delete_address(self) -> None:
        """Test if the address is deleted"""
        self.create_address(2)
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.get_tokens(3).get("testuser2", "")
        )
        response: Response = self.client.delete(self.address_detail_url(2))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_address_with_no_user_associated(self) -> None:
        """Test if the address is deleted with no user associated"""
        self.create_address(3)
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.get_tokens(4).get("testuser2", "")
        )
        response: Response = self.client.delete(self.address_detail_url(1))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_address_with_wrong_id(self) -> None:
        """Test if the address is deleted with wrong address id"""
        self.create_address(3)
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.get_tokens(5).get("testuser2", "")
        )
        response: Response = self.client.delete(self.address_detail_url(4))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class AddressGetTest(BaseTest):
    """Test class for addres information"""

    def test_get_address_detail(self) -> None:
        """Test if addres detail can corretcly be retreived"""
        self.create_address(2)
        address_id: int = 1

        token: str = self.get_tokens(1).get("testuser1", "")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        response: Response = self.client.get(self.address_detail_url(address_id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("street"), "teststreet" + str(address_id))
        self.assertEqual(response.data.get("city"), "testcity" + str(address_id))
        self.assertEqual(response.data.get("state"), "CA")
        self.assertEqual(response.data.get("zip_code"), "l5859")
        self.assertEqual(response.data.get("number"), "testnumber" + str(address_id))

    def test_get_address_with_no_user_associated(self) -> None:
        """Test if addres detail can corretcly be retreived"""
        self.create_address(3)
        tokens: dict[str, str] = self.get_tokens(2)
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + tokens.get("testuser1", "")
        )
        address_id: int = 2
        response: Response = self.client.get(self.address_detail_url(address_id))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
