""" This file contains the views for the users app. """

from typing import Iterable

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth import authenticate

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authtoken.models import Token

from users.models import User, Address
from users.serializers import UserSerializer, AddressSerializer


PERMISSION_ERROR: str = "You do not have permission to perform this action."


class SignupView(APIView):
    """This view is used to create a new user."""

    def post(self, request: Request) -> Response:
        """Create a new user."""
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """This view is used to authenticate a user."""

    def post(self, request: Request) -> Response:
        """Authenticate a user."""
        if (
            not request.data.get("username")
            or not request.data.get("password")
            or not request.data.get("email")
        ):
            return Response(
                {"error": "Username, password and email are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer: UserSerializer = UserSerializer(instance=request.data)

        user: User | AbstractBaseUser | None = authenticate(
            username=serializer.data.get("username"),
            password=serializer.data.get("password"),
            email=serializer.data.get("email"),
        )

        if user is None:
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )

        if isinstance(user, User):
            token: Token = get_object_or_404(Token, user=user)
            return Response(
                {"message": "Login successful", "token": token.key},
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserListView(APIView):
    """This view is used to get all users."""

    # TODO: Add Admin permissions
    permission_classes = [IsAdminUser]

    def get(self, _request: Request) -> Response:
        """Get all users."""
        users: Iterable = User.objects.all()
        serializer: UserSerializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserDetailView(APIView):
    """This view is used to get, update and delete a user."""

    # TODO: Add Admin permissions
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request: Request, pk: int) -> Response:
        """Get a user."""
        if request.user.pk != pk or not request.user.is_staff:
            return Response(status=status.HTTP_403_FORBIDDEN)
        user: User = get_object_or_404(User, pk=pk)
        serializer: UserSerializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request: Request, pk: int) -> Response:
        """Update a user."""
        if request.user.pk != pk or not request.user.is_staff:
            return Response(status=status.HTTP_403_FORBIDDEN)
        user: User = get_object_or_404(User, pk=pk)
        serializer: UserSerializer = UserSerializer(instance=user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, pk: int) -> Response:
        """Delete a user."""
        if request.user.pk != pk or not request.user.is_staff:
            return Response(status=status.HTTP_403_FORBIDDEN)
        user: User = get_object_or_404(User, pk=pk)
        user.delete()
        return Response(status=status.HTTP_200_OK)


class AddressListView(APIView):
    """This view is used to get all addresses and create a new address."""

    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        """Get all addresses."""
        if isinstance(request.user, User) and not request.user.is_staff:
            return Response(
                {"error": PERMISSION_ERROR},
                status=status.HTTP_403_FORBIDDEN,
            )
        addresses: Iterable = Address.objects.all()
        serializer: AddressSerializer = AddressSerializer(addresses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        """Create a new address."""
        serializer: AddressSerializer = AddressSerializer(data=request.data)

        if serializer.is_valid() and isinstance(request.user, User):
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddressDetailView(APIView):
    """This view is used to get, update and delete an address."""

    permission_classes = [IsAuthenticated]

    def get(self, request: Request, pk: int) -> Response:
        """Get an address."""
        address: Address = get_object_or_404(Address, pk=pk)
        if (
            isinstance(request.user, User)
            and address.user != request.user
            and not request.user.is_staff
        ):
            return Response(
                {"error": PERMISSION_ERROR},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer: AddressSerializer = AddressSerializer(address)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request: Request, pk: int) -> Response:
        """Update an address."""
        address: Address = get_object_or_404(Address, pk=pk)
        if (
            isinstance(request.user, User)
            and address.user != request.user
            and not request.user.is_staff
        ):
            return Response(
                {"error": PERMISSION_ERROR}, status=status.HTTP_403_FORBIDDEN
            )

        serializer: AddressSerializer = AddressSerializer(
            instance=address, data=request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, pk: int) -> Response:
        """Delete an address."""
        address: Address = get_object_or_404(Address, pk=pk)
        if (
            isinstance(request.user, User)
            and address.user != request.user
            and not request.user.is_staff
        ):
            return Response(
                {"error": PERMISSION_ERROR},
                status=status.HTTP_403_FORBIDDEN,
            )

        address.delete()
        return Response(
            {"message": "Address deleted successfully"}, status=status.HTTP_200_OK
        )
