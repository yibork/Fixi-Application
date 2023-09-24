from rest_framework import serializers
from .models import User
from dj_rest_auth.registration.serializers import RegisterSerializer as RestAuthRegisterSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email','role']



class RegisterSerializer(RestAuthRegisterSerializer):
    # username = serializers.py.CharField()
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


    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ['username']
