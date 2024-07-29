from typing import Iterable

from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import authenticate

from users.models import User, Address
from users.serializers import UserSerializer, AddressSerializer


class SignupView(APIView):

    def post(self,request:Request) -> Response:
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self,request:Request) -> Response:
        username:str|None = request.data.get('username')
        password:str|None = request.data.get('password')
        user:User|None = authenticate(username=username, password=password)
        print(User.objects.get(username=username))

        if isinstance(user, User):
            token:Token = get_object_or_404(Token, user=user)
            return Response({'token': token.key}, status=HTTP_200_OK)

        return Response(status=HTTP_400_BAD_REQUEST)

class UserListView(APIView):

    permission_classes = [IsAuthenticated]
    def get(self, request:Request) -> Response:
        print(request.user)
        users:Iterable = User.objects.all()
        serializer:UserSerializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=HTTP_200_OK)


class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request:Request, pk:int) -> Response:
        user:User = get_object_or_404(User, pk=pk)
        serializer:UserSerializer = UserSerializer(user)
        return Response(serializer.data, status=HTTP_200_OK)

    def put(self, request:Request, pk:int) -> Response:
        user:User = get_object_or_404(User, pk=pk)
        serializer:UserSerializer = UserSerializer(instance=user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def delete(self, request:Request, pk:int) -> Response:
        user:User = get_object_or_404(User, pk=pk)
        user.delete()
        return Response(status=HTTP_200_OK)

