""" This module contains the test cases for the OrderStatus class. """

from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status

from shopping_and_payments.tests.base import BaseTestCase
from shopping_and_payments.models import OrderStatus


class TestOrderStatus(BaseTestCase):
    """Test cases for the OrderStatus class"""

    def test_create_order_status_view(self) -> None:
        """Test creating an order status"""

        token: str = Token.objects.get(user=self.create_superuser()).key

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")

        response: Response = self.client.post(
            self.order_status_url, {"name": "pending"}
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(OrderStatus.objects.count(), 1)

    def test_create_order_status_as_non_admin(self) -> None:
        """Test creating an order status as a non-admin user"""
        token: str = Token.objects.get(user=self.create_users(1)[0]).key

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")

        response: Response = self.client.post(
            self.order_status_url, {"name": "pending"}
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(OrderStatus.objects.count(), 0)
        self.assertEqual(
            response.data,
            {"detail": "You do not have permission to perform this action."},
        )

    def test_create_order_status_with_invalid_name(self) -> None:
        """Test creating an order status with an invalid name"""
        token: str = Token.objects.get(user=self.create_superuser()).key

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")

        response: Response = self.client.post(
            self.order_status_url, {"name": "invalid"}
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(OrderStatus.objects.count(), 0)
        self.assertEqual(response.data, {"name": ["Invalid status name."]})
