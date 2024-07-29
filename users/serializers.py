from typing import override, Any

from rest_framework.serializers import ModelSerializer
from rest_framework.authtoken.models import Token

from users.models import User,Address

class UserSerializer(ModelSerializer):
    @override
    def create(self, validated_data:dict[str,Any]) -> User:
        password:str|None = validated_data.get('password')
        user = super().create(validated_data)
        user.set_password(raw_password=password)
        user.save()

        Token.objects.create(user=user)
        return user
    
    
    class Meta:
        model = User
        fields = '__all__'

class AddressSerializer(ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


