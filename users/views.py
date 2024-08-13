""" This file contains the views for the users app. """

from typing import Iterable

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import AnonymousUser, AbstractBaseUser
from django.contrib.auth import authenticate

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_201_CREATED,
    HTTP_403_FORBIDDEN,
)
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authtoken.models import Token

from users.models import User, Address
from users.serializers import UserSerializer, AddressSerializer


class SignupView(APIView):
    """This view is used to create a new user."""

    def post(self, request: Request) -> Response:
        """Create a new user."""
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """This view is used to authenticate a user."""

    def post(self, request: Request) -> Response:
        """Authenticate a user."""
        username: str | None = request.data.get("username")
        password: str | None = request.data.get("password")
        user: User | AbstractBaseUser | None = authenticate(
            username=username, password=password
        )

        if isinstance(user, User):
            token: Token = get_object_or_404(Token, user=user)
            return Response({"token": token.key}, status=HTTP_200_OK)

        return Response(status=HTTP_400_BAD_REQUEST)


class UserListView(APIView):
    """This view is used to get all users."""

    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        """Get all users."""
        print(request.user)
        users: Iterable = User.objects.all()
        serializer: UserSerializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=HTTP_200_OK)


class UserCreateAddressView(APIView):
    """This view is used to create an address for a user."""

    permission_classes = [IsAuthenticated]

    def post(self, request: Request) -> Response:
        """Create an address for a user."""
        user: User | AnonymousUser | AbstractBaseUser = request.user
        serializer: AddressSerializer = AddressSerializer(data=request.data)
        if serializer.is_valid() and isinstance(user, User):
            serializer.save(user=user)
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(status=HTTP_400_BAD_REQUEST)


class UserDetailView(APIView):
    """This view is used to get, update and delete a user."""

    permission_classes = [IsAuthenticated]

    def get(self, _request: Request, pk: int) -> Response:
        """Get a user."""
        user: User = get_object_or_404(User, pk=pk)
        serializer: UserSerializer = UserSerializer(user)
        return Response(serializer.data, status=HTTP_200_OK)

    def put(self, request: Request, pk: int) -> Response:
        """Update a user."""
        user: User = get_object_or_404(User, pk=pk)
        serializer: UserSerializer = UserSerializer(instance=user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, pk: int) -> Response:
        """Delete a user."""
        if request.user.pk != pk:
            return Response(status=HTTP_403_FORBIDDEN)
        user: User = get_object_or_404(User, pk=pk)
        user.delete()
        return Response(status=HTTP_200_OK)


class AddressListView(APIView):
    """This view is used to get all addresses and create a new address."""

    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        """Get all addresses."""
        addresses: Iterable = Address.objects.filter(user=request.user)
        serializer: AddressSerializer = AddressSerializer(addresses, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    def post(self, request: Request) -> Response:
        """Create a new address."""
        serializer: AddressSerializer = AddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class AddressDetailView(APIView):
    """This view is used to get, update and delete an address."""

    permission_classes = [IsAuthenticated]

    def get(self, request: Request, pk: int) -> Response:
        """Get an address."""
        address: Address = get_object_or_404(Address, pk=pk)
        if address.user != request.user:
            return Response(status=HTTP_403_FORBIDDEN)
        serializer: AddressSerializer = AddressSerializer(address)
        return Response(serializer.data, status=HTTP_200_OK)

    def put(self, request: Request, pk: int) -> Response:
        """Update an address."""
        address: Address = get_object_or_404(Address, pk=pk)
        if address.user != request.user:
            return Response(status=HTTP_403_FORBIDDEN)
        serializer: AddressSerializer = AddressSerializer(
            instance=address, data=request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, pk: int) -> Response:
        """Delete an address."""
        address: Address = get_object_or_404(Address, pk=pk)
        if address.user != request.user:
            return Response(status=HTTP_403_FORBIDDEN)
        address.delete()
        return Response(status=HTTP_200_OK)
