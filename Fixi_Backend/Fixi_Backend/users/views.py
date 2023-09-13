from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from .serializers import AddressSerializer, UserSerializer
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from .models import Address
from .models import User
from rest_framework.decorators import api_view

import jwt, datetime
class UserAddressViewSet(ModelViewSet):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)


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
