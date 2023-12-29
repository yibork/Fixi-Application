from django.urls import path, include
from rest_framework import routers
from .views import ServiceViewSet,TaxonomyViewSet,FixiServiceViewSet

app_name = "Fixi_Backend.Catalogue"

router = routers.DefaultRouter()
router.register('services', ServiceViewSet, basename='Services')
router.register('taxonomies', TaxonomyViewSet, basename='Taxonomies')
router.register('fixiservices', FixiServiceViewSet, basename='FixiServices')
urlpatterns = router.urls
