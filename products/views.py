"""Views to manage the products app"""

from typing import Iterable
from django.shortcuts import get_list_or_404, get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_201_CREATED,
    HTTP_200_OK,
    HTTP_204_NO_CONTENT,
)

from products.models import Product, Category
from products.serializers import ProductSerializer, CategorySerializer


class CategoryListView(APIView):
    """To get all the categories and create a new one"""

    def get(self, _request: Request) -> Response:
        """Get all the categories"""
        categories: Iterable = get_list_or_404(Category)
        serializer: CategorySerializer = CategorySerializer(
            instance=categories, many=True
        )
        return Response(serializer.data, HTTP_200_OK)

    def post(self, request: Request) -> Response:
        """Create a new Category"""
        serializer: CategorySerializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, HTTP_201_CREATED)
        return Response(serializer.errors, HTTP_400_BAD_REQUEST)


class ProductListView(APIView):
    """View class to create a product and get a list of all of them"""

    def get(self, _request: Request) -> Response:
        """Get all the products"""
        products: Iterable = get_list_or_404(Product)
        serializer: ProductSerializer = ProductSerializer(instance=products, many=True)
        return Response(serializer.data, HTTP_200_OK)

    def post(self, request: Request) -> Response:
        """Create a new product"""
        category_name: str = request.data.pop("category")
        category: Category = get_object_or_404(Category, category_name=category_name)
        serializer: ProductSerializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(category=category)
            return Response(serializer.data, HTTP_201_CREATED)
        return Response(serializer.errors, HTTP_400_BAD_REQUEST)


class ProductDetailView(APIView):
    """View to manage get,put and delete products by id"""

    def get(self, _request: Request, pk: int) -> Response:
        """Get a single product by id"""
        products: Product = get_object_or_404(Product, pk=pk)
        serializer: ProductSerializer = ProductSerializer(instance=products)
        return Response(serializer.data, HTTP_200_OK)

    def put(self, request: Request, pk: int) -> Response:
        """Update a product"""
        category_name: str = request.data.pop("category")
        category: Category = get_object_or_404(Category, category_name=category_name)
        product: Product = get_object_or_404(Product, pk=pk)
        serializer: ProductSerializer = ProductSerializer(
            instance=product, data=request.data
        )
        if serializer.is_valid():
            serializer.save(category=category)
            return Response(serializer.data, HTTP_200_OK)
        return Response(serializer.errors, HTTP_400_BAD_REQUEST)

    def delete(self, _request: Request, pk: int) -> Response:
        """Delete a product by id"""
        product: Product = get_object_or_404(Product, pk=pk)
        product.delete()
        return Response(HTTP_204_NO_CONTENT)
