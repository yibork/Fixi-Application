from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BasketViewSet, BasketItemViewSet, BasketItemCreateView,CartViewSet
app_name = "basket"

router = DefaultRouter()
router.register(r'/basket', BasketViewSet, basename='basket')
router.register(r'/basket-item', BasketItemViewSet, basename='basket-item')
router.register(r'/basket-item-create', BasketItemCreateView, basename='basket-item-create')
router.register(r'/cart', CartViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
