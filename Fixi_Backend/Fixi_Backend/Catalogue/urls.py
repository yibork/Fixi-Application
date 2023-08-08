from django.urls import path, include
from rest_framework import routers
from .views import ServiceViewSet,TaxonomyViewSet

app_name = "Fixi_Backen.Catalogue"

router = routers.DefaultRouter()
router.register('Services', ServiceViewSet, basename='Services')
router.register('Taxonomies', TaxonomyViewSet, basename='Taxonomies')
urlpatterns = router.urls
