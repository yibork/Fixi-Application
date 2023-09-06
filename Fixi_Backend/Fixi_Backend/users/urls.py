from django.urls import path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from .views import (
    LoginView,
)

app_name = "users"
router = routers.DefaultRouter()

urlpatterns = [
    path("refresh/",view = TokenRefreshView.as_view(), name="refresh"),
    path("token/",view = TokenObtainPairView.as_view(), name="token"),
]
urlpatterns += router.urls