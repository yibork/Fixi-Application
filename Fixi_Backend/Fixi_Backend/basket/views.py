from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import Basket  # Import your Basket model
from ..Catalogue.models import Service  # Import your Service model
from .serializers import AddServiceToBasketSerializer  # Import your serializer

class AddServiceToBasketView(APIView):
    def post(self, request):
        serializer = AddServiceToBasketSerializer(data=request.data)
        if serializer.is_valid():
            service_id = serializer.validated_data['service_id']
            try:
                service = Service.objects.get(pk=service_id)
            except Service.DoesNotExist:
                return Response({'error': 'Service not found'}, status=status.HTTP_404_NOT_FOUND)

            if request.user.is_authenticated:
                # User is authenticated, add the service to the user's basket
                user_basket, created = Basket.objects.get_or_create(user=request.user)
                user_basket.service = service
                user_basket.save()
            else:
                # User is not authenticated, add the service to the session basket
                session_key = request.session.session_key
                if not session_key:
                    request.session.save()
                session_basket, created = Basket.objects.get_or_create(session_key=session_key)
                session_basket.service = service
                session_basket.save()

            return Response({'message': 'Service added to basket'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
