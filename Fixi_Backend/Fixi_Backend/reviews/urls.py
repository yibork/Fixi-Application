from django.urls import path, include
from rest_framework import routers
from .views import ReviewReportCreateAPIView,ReviewMediaViewSet,ReviewViewSet

app_name = "Fixi_Backend.reviews"

router = routers.DefaultRouter()
router.register('/review-report', ReviewReportCreateAPIView, basename='Reviewreport')
router.register('/review-media', ReviewMediaViewSet, basename='Reviewmedia')
router.register('/review', ReviewViewSet, basename='Review')

urlpatterns = router.urls
