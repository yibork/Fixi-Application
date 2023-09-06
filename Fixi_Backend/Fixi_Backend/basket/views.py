from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import Basket, BasketItem, Cart
from Fixi_Backend.users.models import User
from .helpers import CartHelper

from .serializers import BasketSerializer, BasketItemSerializer, BasketItemCreateSerializer, CartSerializer
from rest_framework.views import APIView

class BasketViewSet(viewsets.ModelViewSet):
    queryset = Basket.objects.all()
    serializer_class = BasketSerializer

    @action(detail=True, methods=['post'])
    def apply_promo_code(self, request, pk=None):
        basket = self.get_object()
        promo_code = request.data.get('promo_code')

        # Implement promo code logic here
        # Apply promo code to the basket and update its attributes if needed

        return Response({"message": "Promo code applied successfully"})

    @action(detail=True, methods=['post'])
    def add_item(self, request, pk=None):
        basket = self.get_object()
        serializer = BasketSerializer()

        if serializer.is_valid():
            # Create the basket item
            basket_item = serializer.save(basket=basket)
            # Serialize the created basket item and return it in the response
            response_serializer = BasketItemSerializer(basket_item)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def remove_item(self, request, pk=None):
        basket = self.get_object()
        item_id = request.data.get('item_id')

        try:
            item = BasketItem.objects.get(pk=item_id, basket=basket)
            item.delete()
            return Response({"message": "Item removed successfully"})
        except BasketItem.DoesNotExist:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'])
    def clear_basket(self, request, pk=None):
        basket = self.get_object()
        basket.items.all().delete()
        return Response({"message": "Basket cleared successfully"})

    @action(detail=True, methods=['post'])
    def checkout(self, request, pk=None):
        basket = self.get_object()

        # Implement checkout logic here
        # Calculate total, create order, charge payment, etc.

        return Response({"message": "Checkout successful"})
class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all().order_by('id')
    serializer_class = CartSerializer

    @action(methods=['get'], detail=False, url_path='checkout/(?P<userId>[^/.]+)', url_name='checkout')
    def checkout(self, request, *args, **kwargs):

        try:
            user = User.objects.get(pk=int(kwargs.get('userId')))
        except Exception as e:
            return Response(status=status.HTTP_404_NOT_FOUND,
                            data={'Error': str(e)})

        cart_helper = CartHelper(user)
        checkout_details = cart_helper.prepare_cart_for_checkout()

        if not checkout_details:
            return Response(status=status.HTTP_404_NOT_FOUND,
                            data={'error': 'Cart of user is empty.'})

        return Response(status=status.HTTP_200_OK, data={'checkout_details': checkout_details})

class BasketItemViewSet(viewsets.ModelViewSet):
    queryset = BasketItem.objects.all()
    serializer_class = BasketItemSerializer

    # Override create and update methods to handle basket item addition and update
    def create(self, request, *args, **kwargs):
        basket = Basket.objects.get(pk=request.data.get('basket'))
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save(basket=basket)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BasketItemCreateView(viewsets.ModelViewSet):
    queryset = BasketItem.objects.all()
    serializer_class = BasketItemCreateSerializer

    def create(self, request, *args, **kwargs):
        basket = Basket.objects.get(pk=request.data.get('basket'))
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if(basket.items.filter(service=serializer.validated_data['service']).exists()):
                item = basket.items.get(service=serializer.validated_data['service'])
                item.quantity += serializer.validated_data['quantity']
                item.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            serializer.save(basket=basket)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)