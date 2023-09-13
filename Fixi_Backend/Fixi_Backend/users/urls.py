from django.urls import path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from .views import (
    FacebookLoginApiView,
user_list,
LoginView
)

app_name = "users"
router = routers.DefaultRouter()

urlpatterns = [
    path('', user_list, name='user_list'),
    path("login/", view=LoginView.as_view(), name="login"),
    path("refresh/",view = TokenRefreshView.as_view(), name="refresh"),
    path("token/",view = TokenObtainPairView.as_view(), name="token"),
    path("facebook/",view = FacebookLoginApiView.as_view(), name="facebook"),
]
urlpatterns += router.urls