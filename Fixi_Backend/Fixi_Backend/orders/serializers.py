from rest_framework import serializers
from Fixi_Backend.orders.models import *
# from salesman.checkout.serializers.py import CheckoutSerializer as Checkout
from products.api.serializers import ProductSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    product= ProductSerializer(many=False)
    class Meta:
        model = OrderItem
        fields = [
            'id',
            'status',
            'quantity',
            'product'
        ]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'promo_code',
            'phone_number',
            'is_paid',
            'shipping',
            'total_weight',
            'items'
        ]


class CheckoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'id',
            'promo_code',
            'phone_number',
            'is_paid',
            'shipping',
            'total_weight'
        ]  
                          


