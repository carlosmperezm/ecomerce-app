""" This file contains the views for the shopping_and_payments app. """

from typing import Any, Sequence

from django.http import Http404
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework import status


from shopping_and_payments.models import ShoppingCart
from shopping_and_payments.serializers import (
    OrderStatusSerializer,
    ShoppingCartSerializer,
)
from products.models import Product
from users.models import User

# TODO: Create the views for the shopping_and_payments app


class OrderStatusCreationView(APIView):
    """Create a new order status"""

    permission_classes = [IsAdminUser]

    def post(self, request: Request) -> Response:
        """Create a new order status"""
        serializer = OrderStatusSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddProductsToCartView(APIView):
    """Add products to a shopping cart"""

    permission_classes = [IsAuthenticated]

    def post(self, request: Request, pk: int):
        """Add products to a shopping cart"""

        cart: ShoppingCart = get_object_or_404(ShoppingCart, pk=pk)
        if (
            isinstance(request.user, User)
            and cart.user != request.user
            and not request.user.is_staff
        ):
            return Response(
                {"error": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )

        if not request.data:
            return Response(
                {"error": "No data provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        for product_id, quantity in request.data.items():
            if not isinstance(quantity, int):
                return Response(
                    {"error": "Quantity must be an integer."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            try:
                get_object_or_404(Product, pk=product_id)
            except Http404:
                return Response(
                    {"error": f"Product with id {product_id} does not exist."},
                    status=status.HTTP_404_NOT_FOUND,
                )
            cart.products.add(product_id, through_defaults={"quantity": quantity})

        return Response(
            {"message": "Products added to the cart successfully."},
            status=status.HTTP_201_CREATED,
        )


class ShoppingCartCreationView(APIView):
    """View for shopping cart"""

    permission_classes = [IsAuthenticated]

    def post(self, request: Request) -> Response:
        """Create a new shopping cart"""
        serializer: ShoppingCartSerializer = ShoppingCartSerializer(
            data={"user": request.user.pk}
        )

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ShoppingCartDetailView(APIView):
    """View for shopping cart detail"""

    permission_classes = [IsAuthenticated]

    def get(self, request: Request, pk: int) -> Response:
        """Get all shopping carts"""
        cart: ShoppingCart = get_object_or_404(ShoppingCart, pk=pk)
        if (
            isinstance(request.user, User)
            and cart.user != request.user
            and not request.user.is_staff
        ):
            return Response(
                {"error": "You are not allowed to access this cart."},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = ShoppingCartSerializer(instance=cart)
        return Response(serializer.data)

    # def put(self, request: Request, pk: int) -> Response:
    #     """Update a shopping cart"""
    #     cart: ShoppingCart = get_object_or_404(ShoppingCart, pk=pk)
    #     if (
    #         isinstance(request.user, User)
    #         and cart.user != request.user
    #         and not request.user.is_staff
    #     ):
    #         return Response(
    #             {"error": "You are not allowed to access this cart."},
    #             status=status.HTTP_403_FORBIDDEN,
    #         )

    #     serializer = ShoppingCartSerializer(instance=cart, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)

    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
