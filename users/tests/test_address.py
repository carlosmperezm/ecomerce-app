"""Test module for address creation and detail"""

from rest_framework.response import Response
from rest_framework import status

from users.tests.base import BaseTest


class AddressCreationTest(BaseTest):
    """class for address creation tests"""

    def test_address_creation(self) -> None:
        """Test if the address is created"""
        token: str = self.login()
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
        self.create_address(5)
        address_id: int = 5
        response: Response = self.client.get(self.address_detail_url(address_id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("street"), "teststreet" + str(address_id))
        self.assertEqual(response.data.get("city"), "testcity" + str(address_id))
        self.assertEqual(response.data.get("state"), "CA")
        self.assertEqual(response.data.get("zip_code"), "l5859")
        self.assertEqual(response.data.get("number"), "testnumber" + str(address_id))
