"""Models for products app"""

from typing import override

from django.db.models import (
    Model,
    CharField,
    TextField,
    FloatField,
    IntegerField,
    ForeignKey,
    SET_NULL,
)


class Category(Model):
    """Categories model"""

    category_name: CharField = CharField(max_length=100)


class Product(Model):
    """Product model definiton"""

    name: CharField = CharField(max_length=50)
    description: TextField = TextField(null=True, blank=True)
    price: FloatField = FloatField()
    quantity_in_stock: IntegerField = IntegerField()
    category: ForeignKey = ForeignKey(
        Category, null=True, blank=True, on_delete=SET_NULL
    )

    @override
    def __str__(self) -> str:
        return str(self.name)
