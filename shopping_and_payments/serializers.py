""" This module contains the serializers for the shopping_and_payments app """

from rest_framework.serializers import ModelSerializer, ValidationError

from shopping_and_payments.models import (
    CartItems,
    OrderStatus,
    ShoppingCart,
    ShopOrder,
)


class OrderStatusSerializer(ModelSerializer):
    """Order status serializer"""

    PERMITTED_STATUS: tuple[str, ...] = (
        "pending",
        "processing",
        "completed",
        "cancelled",
    )

    def validate_name(self, value: str) -> str:
        """Validate the name of the order status"""
        if value not in self.PERMITTED_STATUS:
            raise ValidationError("Invalid status name.")
        return value

    class Meta:
        """This class is used to define the fields that will be serialized"""

        model = OrderStatus
        fields = "__all__"


class ShoppingCartSerializer(ModelSerializer):
    """Shopping cart serializer"""

    class Meta:
        """This class is used to define the fields that will be serialized"""

        model = ShoppingCart
        fields = "__all__"


class ShopOrderSerializer(ModelSerializer):
    """Shop order serializer"""

    class Meta:
        """This class is used to define the fields that will be serialized"""

        model = ShopOrder
        fields = "__all__"


class CartItemsSerializer(ModelSerializer):
    """Cart items serializer"""

    class Meta:
        """This class is used to define the fields that will be serialized"""

        model = CartItems
        fields = "__all__"
