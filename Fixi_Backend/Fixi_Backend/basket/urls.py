from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AddServiceToBasketView
app_name = "basket"

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('add_service_to_basket/', AddServiceToBasketView.as_view(), name='add_service_to_basket'),

]
