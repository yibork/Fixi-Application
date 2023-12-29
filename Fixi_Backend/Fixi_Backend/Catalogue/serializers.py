from rest_framework import serializers
from .models import Service, Taxonomy, ServiceTaxonomy, FixiService

from rest_framework import serializers

class ServiceSerializer(serializers.ModelSerializer):
    parent_taxonomies = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = '__all__'

    def get_parent_taxonomies(self, obj):
        service_taxonomies = ServiceTaxonomy.objects.filter(service=obj)
        parent_taxonomies = []

        for st in service_taxonomies:
            parent_taxonomies.extend(self.get_all_parent_taxonomies(st.taxonomy))

        if parent_taxonomies:
            serializer = TaxonomySerializer(parent_taxonomies[0])  # Get the first element
            return serializer.data

        return None

    def get_all_parent_taxonomies(self, taxonomy):
        parent_taxonomies = []
        while taxonomy:
            parent_taxonomies.append(taxonomy)
            taxonomy = taxonomy.get_parent()
        return parent_taxonomies

    def get_all_parent_taxonomies(self, taxonomy):
        parent_taxonomies = []
        while taxonomy:
            parent_taxonomies.append(taxonomy)
            taxonomy = taxonomy.get_parent()
        return parent_taxonomies


class TaxonomySerializer(serializers.ModelSerializer):
    parent = serializers.SerializerMethodField()
#    discount = serializers.py.SerializerMethodField(method_name='get_discount')
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

class FixiServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FixiService
        fields = '__all__'