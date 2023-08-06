from django.urls import path, include
from rest_framework import routers
from .views import CatalogueViewSet

app_name = "Fixi_Backend"

router = routers.DefaultRouter()
router.register('catalogue', CatalogueViewSet, basename='catalogue')

urlpatterns = router.urls
