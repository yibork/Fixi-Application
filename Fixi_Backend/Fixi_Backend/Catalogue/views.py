from rest_framework.viewsets import ModelViewSet
from .models import Service,Taxonomy, FixiService
from .serializers import ServiceSerializer,TaxonomySerializer
from .serializers import FixiServiceSerializer
class ServiceViewSet(ModelViewSet):
    serializer_class = ServiceSerializer
    def get_queryset(self):
        # Return the desired queryset here
        return Service.objects.all()


class TaxonomyViewSet(ModelViewSet):
    serializer_class = TaxonomySerializer

    def get_queryset(self):
        # Return the desired queryset here
        return Taxonomy.objects.all()

class FixiServiceViewSet(ModelViewSet):
    serializer_class = FixiServiceSerializer
    def get_queryset(self):
        # Return the desired queryset here
        return FixiService.objects.all()

