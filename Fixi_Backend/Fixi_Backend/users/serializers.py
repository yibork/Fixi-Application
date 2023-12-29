from rest_framework import serializers
from .models import User
from dj_rest_auth.registration.serializers import RegisterSerializer as RestAuthRegisterSerializer
from rest_framework.authtoken.models import Token
from .models import Review
from rest_framework.authentication import TokenAuthentication

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class CustomTokenAuthentication(TokenAuthentication):
    def create_token(self, user):
        token, created = Token.objects.get_or_create(user=user)
        # Customize the token payload here
        token_payload = {
            'user_id': user.id,
            'email': user.email,
            'username': user.username,
            # Add any other user information you need
        }
        token.token = self.encode_token_payload(token_payload)
        token.save()
        return token

class CustomTokenSerializer(serializers.Serializer):
    token = serializers.CharField()
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        user = self.context['request'].user
        return {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            # Include other user details as needed
        }

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['username'] = user.username
        token['email'] = user.email
        token['role'] = user.role
        token['phone_number'] = user.phone_number
        token['is_superuser'] = user.is_superuser
        return token


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
        fields = ['username', 'email', 'password', 'phone_number', 'picture','first_name','last_name','role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            phone_number=validated_data.get('phone_number'),
            picture=validated_data.get('picture'),
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            role=validated_data.get('role'),
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class ServiceProviderSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    reviews = ReviewSerializer(many=True, read_only=True)
    taxonomy = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id', 'taxonomy','username', 'first_name', 'last_name', 'picture', 'average_rating', 'reviews']

    def get_taxonomy(self, obj):
        return obj.taxonomy.name
    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews:
            total_rating = sum([review.rating for review in reviews])
            return total_rating / len(reviews)
        return 0
