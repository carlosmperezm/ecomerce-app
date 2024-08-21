""" This module contains the serializers for the shopping_and_payments app """

from rest_framework.serializers import (
    ModelSerializer,
    ValidationError,
    SerializerMethodField,
    Serializer,
    IntegerField
)

from shopping_and_payments.models import (
    CartItem,
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

class AddToCartSerializer(Serializer):

    product_id: int = IntegerField()
    quantity: int = IntegerField(min_value=1)


    # def validate(self, data: dict) -> dict:
    #     """Validate the data provided"""
    #     product_id: int = data.get("product_id")
    #     quantity: int = data.get("quantity")
    #
    #     if not product_id:
    #         raise ValidationError("Product ID is required.")
    #
    #     if not quantity:
    #         raise ValidationError("Quantity is required.")
    #
    #     if quantity < 1:
    #         raise ValidationError("Quantity must be greater than 0.")
    #
    #     return data


class CartItemSerializer(ModelSerializer):
    """Cart items serializer"""

    # cart: SerializerMethodField = ShoppingCartSerializer()
    # product: RelatedField = RelatedField(queryset=CartItem.objects.all())

    class Meta:
        """This class is used to define the fields that will be serialized"""


        model = CartItem
        fields = "__all__"
        read_only_fields = ("cart",)

    def get_cart(self, obj: CartItem) -> ShoppingCart:
        """Get the cart to which the cart item belongs"""
        return obj.cart

