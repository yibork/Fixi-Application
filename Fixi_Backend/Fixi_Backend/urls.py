"""Fixi_Backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include

from pictures.conf import get_settings
app_name = "Fixi_Backend"
urlpatterns = [
    path('admin/', admin.site.urls),
    path("reviews", include("Fixi_Backend.reviews.urls")),
    path("service", include("Fixi_Backend.Catalogue.urls")),
    path("basket", include("Fixi_Backend.basket.urls")),
    path("users/", include("Fixi_Backend.users.urls", namespace="users")),
    path('conversations/', include('Fixi_Backend.chat.urls'))  # new

]

