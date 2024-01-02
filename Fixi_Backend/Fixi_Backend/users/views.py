from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer, ReviewSerializer, ServiceProviderSerializer
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from .models import User
from rest_framework.decorators import api_view
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from rest_framework import permissions
import jwt, datetime
from .models import Review
from .permissions import IsServiceProvider  # Custom permission class to check if the user is a service provider

class GoogleLoginApiView(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter


class FacebookLoginApiView(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter

class LoginView(APIView):
    def post(self, request):
        email = request.GET.get('email')
        password = request.GET.get('password')

        user = User.objects.filter(email=email).first()
        if user is None:
            print(user.objects.all())
            return Response({'error': 'Invalid Data'})
            print('Invalid Data')
        if not user.check_password(password):
            return Response({'error': 'Incorrect Password'})
        playload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=15),
            'iat': datetime.datetime.utcnow()
        }
        token = jwt.encode( playload ,'secret',algorithm='HS256')
        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }
        return response

class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(user=self.request.user)

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        data = request.data
        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.phone_number = data.get('phone_number', user.phone_number)
        user.save()
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)

# Create your views here.

@api_view(['GET'])
def user_list(request, ):
    users = User.objects.all().order_by('username')
    serializer = UserSerializer(instance=users, many=True)
    return Response(serializer.data)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['email'] = user.email
        token['id'] = user.id
        token['phone_number'] = user.phone_number




        # ...
        return token
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
class UserRegister(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request):
        print(request.data)
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response({"message":"User Created"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewView(ModelViewSet):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()

class ServiceProviderListView(APIView):
    def get(self, request, format=None):
        service_providers = User.objects.filter(role=User.ServiceProvider)
        serializer = ServiceProviderSerializer(service_providers, many=True)
        return Response(serializer.data)

class UpdateLocationView(APIView):
    permission_classes = [IsServiceProvider]

    def put(self, request, *args, **kwargs):
        user = request.user
        lat = request.data.get('latitude')
        lon = request.data.get('longitude')

        if lat is None or lon is None:
            return Response({'error': 'Latitude and longitude are required.'}, status=status.HTTP_400_BAD_REQUEST)

        user.latitude = float(lat)
        user.longitude = float(lon)
        user.save()
        return Response({'status': 'Location updated successfully.'})

import math

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of the earth in km

    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dLon/2) * math.sin(dLon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = R * c  # Distance in km
    return distance

class ServiceProviderSuggestionView(APIView):
    def get(self, request, *args, **kwargs):
        user_lat = request.query_params.get('latitude')
        user_lon = request.query_params.get('longitude')

        if user_lat is None or user_lon is None:
            return Response({'error': 'Latitude and longitude are required.'}, status=status.HTTP_400_BAD_REQUEST)

        user_lat = float(user_lat)
        user_lon = float(user_lon)
        service_providers = User.objects.filter(role=User.ServiceProvider)
        nearby_service_providers = [sp for sp in service_providers if calculate_distance(user_lat, user_lon, sp.latitude, sp.longitude) <= 15]

        # Serialize the data
        serializer = ServiceProviderSerializer(nearby_service_providers, many=True)
        return Response(serializer.data)
