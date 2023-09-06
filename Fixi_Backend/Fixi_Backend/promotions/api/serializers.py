from rest_framework import serializers
from ..models import PromoCode, UserPromoCode


class PromoCodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = PromoCode
        fields = [
            'id',
            'code',
            'value',
            'type',
        ]


class UserPromoCodeSerializer(serializers.ModelSerializer):
    promo_code = PromoCodeSerializer()
    class Meta:
        model = UserPromoCode
        fields = [
            'id',
            'promo_code'
        ]
