from rest_framework import serializers
from .models import Service, Taxonomy

from rest_framework import serializers

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'name', 'description', 'price', 'image', 'created_by', 'slug']

class TaxonomySerializer(serializers.ModelSerializer):
    parent = serializers.SerializerMethodField()
#    discount = serializers.SerializerMethodField(method_name='get_discount')
    class Meta:
        model = Taxonomy
        fields = [
            'name',
            'slug',
            'parent'
        ]

    def get_parent(self, obj):
        # return obj.get_parent().name if obj.get_parent() else "None"
        parent = obj.get_parent()
        if parent:
            serializer = TaxonomySerializer(parent)  # Serialize the parent using the same serializer
            return serializer.data
        return None
