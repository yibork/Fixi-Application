from rest_framework import serializers
from .models import Basket

class AddServiceToBasketSerializer(serializers.Serializer):
    service_id = serializers.IntegerField()


class BasketSerializer(serializers.ModelSerializer):
    total = serializers.SerializerMethodField()

    class Meta:
        model = Basket
        fields = '__all__'

    def get_total(self, obj):
        return obj.total_price()

