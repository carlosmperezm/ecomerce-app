""" This file contains the views for the shopping_and_payments app. """

from typing import Any
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.db.models import Model

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework import status


from shopping_and_payments.models import CartItem, ShoppingCart,ShopOrder
from shopping_and_payments.serializers import  OrderStatusSerializer, ShoppingCartSerializer, CartItemSerializer,AddToCartSerializer, ShopOrderSerializer
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

        cart: ShoppingCart = None

        if not request.data:
            return Response( {"error": "No data provided."}, status=status.HTTP_400_BAD_REQUEST,)

        try:
            cart: ShoppingCart = ShoppingCart.objects.get(pk=pk)
        except ShoppingCart.DoesNotExist:
            return Response( {"error": "Shopping cart does not exist."}, status=status.HTTP_404_NOT_FOUND,)

        if ( isinstance(request.user, User) and cart.user != request.user and not request.user.is_staff):
            return Response( {"error": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN,)

        serializer:AddToCartSerializer = AddToCartSerializer(data=request.data)

        if serializer.is_valid():
            product_id:int = serializer.validated_data.get("product_id")
            quantity:int = serializer.validated_data.get("quantity")

            try:
                product: Product = Product.objects.get(pk=product_id)
            except Product.DoesNotExist:
                return Response( {"error": f"Product with id {product_id} does not exist."}, status=status.HTTP_404_NOT_FOUND,)

            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

            if not created:
                cart_item.quantity += quantity
                cart_item.save()
            else:
                cart_item.quantity = quantity
                cart_item.save()
            return Response( {"message": "Products added to the cart successfully."}, status=status.HTTP_201_CREATED,)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST,)


class UpdateProductsInCartView(APIView):
    """Update products in a shopping cart"""

    permission_classes = [IsAuthenticated]

    def put(self, request: Request, cart_id: int, item_id: int) -> Response:
        """Update products in a shopping cart"""

        cart: ShoppingCart = get_object_or_404(ShoppingCart, pk=cart_id)
        cart_item: CartItem = get_object_or_404(CartItem, pk=item_id)

        # Validate if the user has permission to update the cart
        if (isinstance(request.user, User) and cart.user != request.user and not request.user.is_staff):
            return Response( {"error": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN,)

        # Validate if the request has data
        if not request.data:
            return Response( {"error": "No data provided."}, status=status.HTTP_400_BAD_REQUEST,)

        # Validate if the new product id is provided
        if request.data.get("new_product_id") is None:
            return Response( {"error": "Product id is required."}, status=status.HTTP_400_BAD_REQUEST,)

        new_product_id: int | Any = request.data.get("new_product_id")
        quantity: int | Any = request.data.get("quantity")

        # Validate if the quantity and new product id are integers
        if not isinstance(quantity, int) or not isinstance(new_product_id, int):
            return Response( {"error": "Quantity and new product id must be integers."}, status=status.HTTP_400_BAD_REQUEST,)

        serializer: CartItemSerializer = CartItemSerializer(instance=cart_item, data={"product": new_product_id, "quantity": quantity},)

        if serializer.is_valid():
            serializer.save()
            return Response( {"message": "Products updated in the cart successfully."}, status=status.HTTP_200_OK)

        return Response( serializer.errors, status=status.HTTP_400_BAD_REQUEST)



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

    def delete(self, request: Request, pk: int) -> Response:
        """Delete a shopping cart"""
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

        cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CreateOrderView(APIView):
    """Create an order"""

    permission_classes = [IsAuthenticated]

    def post(self, request: Request) -> Response:
        """Create an order"""

        serializer: ShopOrderSerializer = ShopOrderSerializer(data=request.data)

        if serializer.is_valid():
            print('Serializer was Valid')
            cart:ShoppingCart = ShoppingCart.objects.get(pk=serializer.validated_data.get('cart').pk)

            if cart.user != request.user:
                return Response( {"error": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
            
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        print('Serializer was not Valid')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
