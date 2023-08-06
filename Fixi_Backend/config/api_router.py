from django.conf import settings
from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter


if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()


urlpatterns = router.urls


urlpatterns += [
    path('auth/', include('dj_rest_auth.urls'), name='auth'),
    path('auth/registration/', include('dj_rest_auth.registration.urls'), name='auth-registration'),
]