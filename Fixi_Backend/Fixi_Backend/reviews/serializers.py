from rest_framework import serializers
from Fixi_Backend.reviews.models import *
from Fixi_Backend.users.serializers import UserSerializer
# from . import UserSerializer


class MediaReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewMedia
        fields = ['id', 'image', 'review']


class ReviewReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewReport
        fields= [
            'user',
            'review',
            'reason',
            'reason_other',
            'message'
        ]

    def validate(self, attrs):
        if attrs['reason'].is_other:
            if not attrs['reason_other'] :
                raise serializers.ValidationError({
                    'reason_other':'This field is required'
                })
        return attrs

    def save(self, review_id,user):
        self.validated_data['review_id'] = review_id
        self.validated_data['user'] = user
        return super().save()


class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    # media = MediaReviewSerializer(source="reviewmedia_set", many=True)

    class Meta:
        model = Review
        fields = (
            'id',
            'stars',
            'title',
            'message',
            'user',
            'votes',
            'category'
        )
        