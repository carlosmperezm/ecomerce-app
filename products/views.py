"""Views to manage the products app"""

from typing import Iterable

from django.shortcuts import get_list_or_404, get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from products.models import Product, Category
from products.serializers import ProductSerializer, CategorySerializer
from users.models import User

PERMISION_ERROR: str = "You do not have permission to perform this action."


class CategoryListView(APIView):
    """To get all the categories and create a new one"""

    def get(self, _request: Request) -> Response:
        """Get all the categories"""
        categories: Iterable = get_list_or_404(Category)
        serializer: CategorySerializer = CategorySerializer(
            instance=categories, many=True
        )
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        """Create a new Category"""

        # Only admin users can create a category
        if isinstance(request.user, User) and request.user.is_staff:
            serializer: CategorySerializer = CategorySerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status.HTTP_201_CREATED)
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        return Response({"error": PERMISION_ERROR}, status.HTTP_403_FORBIDDEN)


class CategoryDetailView(APIView):
    """To get, update and delete a category by id"""

    permission_classes = [IsAdminUser]

    def get(self, _request: Request, pk: int) -> Response:
        """Get a single category by id"""
        category: Category = get_object_or_404(Category, pk=pk)
        serializer: CategorySerializer = CategorySerializer(instance=category)
        return Response(serializer.data, status.HTTP_200_OK)

    def put(self, request: Request, pk: int) -> Response:
        """Update a category"""
        category: Category = get_object_or_404(Category, pk=pk)

        serializer: CategorySerializer = CategorySerializer(
            instance=category, data=request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def delete(self, _request: Request, pk: int) -> Response:
        """Delete a category by id"""
        category: Category = get_object_or_404(Category, pk=pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductListView(APIView):
    """View class to create a product and get a list of all of them"""

    def get(self, _request: Request) -> Response:
        """Get all the products"""
        products: Iterable = get_list_or_404(Product)
        serializer: ProductSerializer = ProductSerializer(instance=products, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        """Create a new product"""
        # You can only create a product if you are authenticated
        if not request.user.is_authenticated:
            return Response({"error": PERMISION_ERROR}, status.HTTP_403_FORBIDDEN)

        category_name: str = request.data.pop("category")
        category: Category = get_object_or_404(Category, category_name=category_name)
        serializer: ProductSerializer = ProductSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(category=category)
            return Response(serializer.data, status.HTTP_201_CREATED)

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class ProductDetailView(APIView):
    """View to manage get,put and delete products by id"""

    def get(self, _request: Request, pk: int) -> Response:
        """Get a single product by id"""
        products: Product = get_object_or_404(Product, pk=pk)
        serializer: ProductSerializer = ProductSerializer(instance=products)
        return Response(serializer.data, status.HTTP_200_OK)

    def put(self, request: Request, pk: int) -> Response:
        """Update a product"""
        self.permission_classes = [IsAuthenticated]
        category_name: str = request.data.pop("category")
        category: Category = get_object_or_404(Category, category_name=category_name)
        product: Product = get_object_or_404(Product, pk=pk)
        serializer: ProductSerializer = ProductSerializer(
            instance=product, data=request.data
        )
        if serializer.is_valid():
            serializer.save(category=category)
            return Response(serializer.data, status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def delete(self, _request: Request, pk: int) -> Response:
        """Delete a product by id"""
        self.permission_classes = [IsAuthenticated]
        product: Product = get_object_or_404(Product, pk=pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
