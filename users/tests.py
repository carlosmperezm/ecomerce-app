"""Tests"""

from typing import override

from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
)

from users.models import User, Address


class BaseTest(APITestCase):
    """Class base to set up all the pervious data and methods"""

    user_data: dict[str, str] = {}
    address_data: dict[str, str] = {}

    def _login(self) -> str:
        self.user_data = {
            "username": "testuser",
            "email": "test@test.com",
            "password": "testpassword",
        }
        self.client.post(reverse("signup"), self.user_data)
        response: Response = self.client.post(reverse("login"), self.user_data)
        return response.data.get("token")

    def _create_address(self) -> Address:
        self.address_data: dict[str, str] = {
            "street": "teststreet",
            "city": "testcity",
            "state": "CA",
            "zip_code": "l5859",
            "number": "testnumber",
        }
        token: str = self._login()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        self.client.post(reverse("address-list"), self.address_data)
        address: Address = Address.objects.get(street=self.address_data.get("street"))
        return address


class UserCreateAddressTest(BaseTest):
    """Test for user address creation"""

    @override
    def setUp(self) -> None:
        self.address_data = {
            "street": "teststreet",
            "city": "testcity",
            "state": "CA",
            "zip_code": "l5859",
            "number": "testnumber",
        }
        token: str = self._login()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        self.url: str = reverse("user-create-address")

    def test_user_create_address(self) -> None:
        """test if and address can be created"""
        response: Response = self.client.post(self.url, self.address_data)
        self.assertEqual(response.status_code, HTTP_201_CREATED)


class SigUpTest(BaseTest):
    """Test class if the user can sign up"""

    @override
    def setUp(self) -> None:
        self.user_data = {
            "username": "testuser",
            "email": "test@test.com",
            "password": "testpassword",
            # 'phone_number': '1234567890',
            # 'address': self._create_address(),
        }

        self.url: str = reverse("signup")

        return super().setUp()

    def test_signup(self) -> None:
        """sign up the user"""
        response: Response = self.client.post(self.url, self.user_data)
        self.client.put(
            reverse("user-detail", args=[1]), {"address": self._create_address().id}
        )

        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(response.data.get("username"), self.user_data.get("username"))
        self.assertEqual(response.data.get("email"), self.user_data.get("email"))
        self.assertEqual(
            response.data.get("phone_number"), self.user_data.get("phone_number")
        )
        # self.assertEqual(response.data.get('address'), self.user_data.get('address'))

    def test_signup_invalid_data(self) -> None:
        """test if the user insert not data the api responds with a 400 error code"""
        response: Response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)


class LoginTest(BaseTest):
    """class for login tests"""

    @override
    def setUp(self) -> None:
        self.user_data = {
            "username": "testuser",
            "email": "test@test.com",
            "password": "testpassword",
        }

        self.url: str = reverse("login")
        self.client.post(reverse("signup"), self.user_data)

    def test_login(self) -> None:
        """test if the user has logged correctly"""
        response: Response = self.client.post(self.url, self.user_data)
        user: User = User.objects.get(username=self.user_data.get("username"))

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data.get("token"), user.auth_token.key)

    def test_login_invalid_data(self) -> None:
        """Check if the user no insert any data to log in
        the porgram should respond with a 400 error code"""
        response: Response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertIsNone(response.data)

    def test_login_invalid_user(self) -> None:
        """test if the user insert no valid password or no valid username
        The program should return 400 bad request"""
        response: Response = self.client.post(
            self.url, {"username": "invaliduser", "password": "invalidpassword"}
        )
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertIsNone(response.data)


class AddressCreationTest(BaseTest):
    """class for address creation tests"""

    @override
    def setUp(self) -> None:
        self.address_data = {
            "street": "teststreet",
            "city": "testcity",
            "state": "CA",
            "zip_code": "l5859",
            "number": "testnumber",
        }
        self.url: str = reverse("address-list")

    def test_address_creation(self) -> None:
        """Test if the address is created"""
        token: str = self._login()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        response: Response = self.client.post(self.url, self.address_data)

        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(response.data.get("street"), self.address_data.get("street"))
        self.assertEqual(response.data.get("city"), self.address_data.get("city"))
        self.assertEqual(response.data.get("state"), self.address_data.get("state"))
        self.assertEqual(
            response.data.get("zip_code"), self.address_data.get("zip_code")
        )
        self.assertEqual(response.data.get("number"), self.address_data.get("number"))


class AddressDetailTest(BaseTest):
    """Test class for addres information"""

    @override
    def setUp(self) -> None:
        self.address_data = {
            "street": "teststreet",
            "city": "testcity",
            "state": "CA",
            "zip_code": "l5859",
            "number": "testnumber",
        }
        self.url: str = reverse("address-list")
        token = self._login()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        response: Response = self.client.post(self.url, self.address_data)
        self.address_id: int = response.data.get("id")
        self.url = reverse("address-detail", args=[self.address_id])

    def test_address_detail(self) -> None:
        """Test if addres detail can corretcly be retreived"""
        response: Response = self.client.get(self.url)
        # print(response.data)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data.get("street"), self.address_data.get("street"))
        self.assertEqual(response.data.get("city"), self.address_data.get("city"))
        self.assertEqual(response.data.get("state"), self.address_data.get("state"))
        self.assertEqual(
            response.data.get("zip_code"), self.address_data.get("zip_code")
        )
        self.assertEqual(response.data.get("number"), self.address_data.get("number"))
