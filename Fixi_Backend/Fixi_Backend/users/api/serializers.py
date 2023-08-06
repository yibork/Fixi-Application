from rest_framework import serializers
from ..models import User, Address
from dj_rest_auth.registration.serializers import RegisterSerializer as RestAuthRegisterSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'name',
            'first_name',
            'last_name',
            'is_verified',
            'verify_token',
            'phone_number',
            'wishlist',
        ]


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            'id',
            'address',
            'city',
            'is_primary',
            'zip'
        ]


class RegisterSerializer(RestAuthRegisterSerializer):
    # username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username',''),
            'first_name': self.validated_data.get('first_name',''),
            'last_name': self.validated_data.get('last_name',''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
        }