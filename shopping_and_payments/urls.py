""" This file contains the URL patterns for the shopping_and_payments app. """

from django.urls import path

from shopping_and_payments.views import (
    OrderStatusCreationView,
    ShoppingCartCreationView,
    ShoppingCartDetailView,
    AddProductsToCartView,
)

urlpatterns = [
    path(
        "order-status/create/",
        OrderStatusCreationView.as_view(),
        name="order_status_create",
    ),
    path(
        "shopping-cart/",
        ShoppingCartCreationView.as_view(),
        name="create_shopping_cart",
    ),
    path(
        "shopping-cart/<int:pk>/",
        ShoppingCartDetailView.as_view(),
        name="shopping_cart",
    ),
    path(
        "add-products-to-cart/<int:pk>/",
        AddProductsToCartView.as_view(),
        name="add_products_to_cart",
    ),
]
