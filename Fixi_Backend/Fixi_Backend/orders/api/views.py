from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from rest_framework.response import Response
from .serializers import OrderSerializer
from rest_framework.permissions import IsAuthenticated
from ..models import Order

class OrderViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def update(self, request, *args, **kwargs):
        order = self.get_object()
        data = request.data
        order.promo_code = data.get('promo_code', order.promo_code)
        order.phone_number = data.get('phone_number', order.phone_number)
        order.is_paid = data.get('is_paid', order.is_paid)
        order.shipping_id = data.get('shipping', order.shipping_id)
        order.save()
        return Response(OrderSerializer(order).data, status=status.HTTP_200_OK)
