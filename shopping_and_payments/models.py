"""This module contains the models for the shopping_and_payments app"""

from typing import override

from django.db.models import (
    CharField,
    Model,
    IntegerField,
    OneToOneField,
    ForeignKey,
    CASCADE,
    DateTimeField,
    ManyToManyField,
    PositiveIntegerField,
    Manager,
)


class OrderStatus(Model):
    """Order status model"""

    name: CharField = CharField(max_length=50)

    objects = Manager()

    @override
    def __str__(self) -> str:
        return str(self.name)


class ShoppingCart(Model):
    """Shopping cart model"""

    user: OneToOneField = OneToOneField("users.User", on_delete=CASCADE)
    products: ManyToManyField = ManyToManyField("products.Product", through="CartItems")
    created_at: DateTimeField = DateTimeField(auto_now_add=True)

    objects = Manager()

    @override
    def __str__(self) -> str:
        return f"Cart #{self.pk} and belongs to {self.user}"


class CartItems(Model):
    """Cart items model"""

    cart: ForeignKey = ForeignKey(ShoppingCart, on_delete=CASCADE)
    product: ForeignKey = ForeignKey("products.Product", on_delete=CASCADE)
    quantity: IntegerField = PositiveIntegerField()

    objects = Manager()

    @override
    def __str__(self) -> str:
        return f"CartItem #{self.pk} in {self.cart}"


class ShopOrder(Model):
    """Shop order model"""

    cart: OneToOneField = OneToOneField(ShoppingCart, on_delete=CASCADE)
    status: ForeignKey = ForeignKey(OrderStatus, on_delete=CASCADE)
    total_price: IntegerField = IntegerField()
    order_date: DateTimeField = DateTimeField(auto_now_add=True)

    objects = Manager()

    def __str__(self) -> str:
        return f"shop order # {self.pk}"
