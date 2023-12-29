from django.urls import path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from .views import UserRegister, MyTokenObtainPairView, ReviewView, ServiceProviderListView

from .views import (
    FacebookLoginApiView,
user_list,
LoginView
)

app_name = "users"
router = routers.DefaultRouter()
router.register('reviews', ReviewView, basename='Reviews')
urlpatterns = [
    path('', user_list, name='user_list'),
    path("refresh/",view = TokenRefreshView.as_view(), name="refresh"),
    path("token/",view = TokenObtainPairView.as_view(), name="token"),
    path("facebook/",view = FacebookLoginApiView.as_view(), name="facebook"),
    path('register/', UserRegister.as_view(), name='register'),
    path('login/', MyTokenObtainPairView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('service-providers/', ServiceProviderListView.as_view(), name='service-providers'),

]
urlpatterns += router.urls