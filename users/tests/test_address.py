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


class AddressDetailTest(BaseTest):
    """Test class for addres information"""

    def test_address_detail(self) -> None:
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

    def test_get_address_with_no_user_associed(self) -> None:
        """Test if addres detail can corretcly be retreived"""
        self.create_address(3)
        tokens: dict[str, str] = self.get_tokens(2)
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + tokens.get("testuser1", "")
        )
        address_id: int = 2
        response: Response = self.client.get(self.address_detail_url(address_id))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_address(self) -> None:
        """Test if the address is deleted"""
        # TODO

    def test_delete_address_with_no_user_associed(self) -> None:
        """Test if the address is deleted"""
        # TODO

    def test_update_address(self) -> None:
        """Test if the address is updated"""
        # TODO

    def test_update_address_with_no_user_associed(self) -> None:
        """Test if the address is updated"""
        # TODO
