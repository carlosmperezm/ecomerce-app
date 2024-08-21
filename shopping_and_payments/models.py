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
    products: ManyToManyField = ManyToManyField(
        "products.Product", through="CartItem", blank=True, default=None
    )
    created_at: DateTimeField = DateTimeField(auto_now_add=True)

    objects = Manager()

    @override
    def __str__(self) -> str:
        return f"Cart #{self.pk} and belongs to {self.user}"


class CartItem(Model):
    """Cart items model"""

    cart: ForeignKey = ForeignKey(ShoppingCart, on_delete=CASCADE)
    product: ForeignKey = ForeignKey(
        "products.Product", on_delete=CASCADE, null=True, blank=True, default=None
    )
    quantity: IntegerField = PositiveIntegerField(default=1)

    objects = Manager()

    @override
    def __str__(self) -> str:
        return f"CartItem #{self.pk} in {self.cart}"


class ShopOrder(Model):
    """Shop order model"""

    def total_price(self) -> int:
        """Return the total price of the order"""
        result:int|float = 0

        for product in self.cart.products.all():
            result += product.price
        
        return result

    cart: OneToOneField = OneToOneField(ShoppingCart, on_delete=CASCADE)
    status: ForeignKey = ForeignKey(OrderStatus, on_delete=CASCADE,default=1)
    total_price: int = total_price
    order_date: DateTimeField = DateTimeField(auto_now_add=True)

    objects = Manager()



    def __str__(self) -> str:
        return f"shop order # {self.pk}"
