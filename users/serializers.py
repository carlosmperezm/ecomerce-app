"""Users app serializers"""

from typing import override, Any

from rest_framework.serializers import ModelSerializer
from rest_framework.authtoken.models import Token

from users.models import User, Address


class AddressSerializer(ModelSerializer):
    """Serializer for each addresses"""

    class Meta:
        """Create the class fields automatically"""

        model = Address
        fields = "__all__"


class UserSerializer(ModelSerializer):
    """Serializer for each users"""

    address: AddressSerializer = AddressSerializer(required=False)

    @override
    def create(self, validated_data: dict[str, Any]) -> User:
        password: str | None = validated_data.get("password")
        user = User.objects.create(**validated_data)
        user.set_password(raw_password=password)
        user.save()

        Token.objects.create(user=user)
        return user

    class Meta:
        """Create the class fields automatically"""

        model = User
        fields = "__all__"
