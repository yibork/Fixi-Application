from rest_framework import serializers
from ..Catalogue.serializers import ServiceSerializer
from .models import Basket, BasketItem, Cart

class BasketItemSerializer(serializers.ModelSerializer):
    service = ServiceSerializer(read_only=True)
    class Meta:
        model = BasketItem
        fields = ['id','basket','service','quantity']

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'user', 'item', 'quantity', 'created_at', 'updated_at']


class BasketSerializer(serializers.ModelSerializer):
    items = BasketItemSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = Basket
        fields = '__all__'

    def get_total(self, obj):
        return obj.total_price()

    def to_representation(self, instance):
        # Check if the user making the request is the owner of the basket
        user = self.context['request'].user

        if user == instance.user:
            return super().to_representation(instance)
        else:
            # Return an empty representation or raise a permission error as needed
            return {}

class BasketItemCreateSerializer(serializers.ModelSerializer):
    # Define a serializer for the 'add_item' action
    class Meta:
        model = BasketItem
        fields = ['service', 'quantity','basket']
