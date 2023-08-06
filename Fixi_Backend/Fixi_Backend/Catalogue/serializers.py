from rest_framework import serializers
from .models import Catalogue


class CatalogueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Catalogue
        fields = ['id', 'name', 'description', 'price', 'image', 'created_by']