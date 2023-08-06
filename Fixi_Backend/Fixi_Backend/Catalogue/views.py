from rest_framework.viewsets import ModelViewSet
from .models import Catalogue
from .serializers import CatalogueSerializer
from django.db.models import Q

class CatalogueViewSet(ModelViewSet):
    serializer_class = CatalogueSerializer

    def get_queryset(self):
        # Return the desired queryset here
        return Catalogue.objects.all()
