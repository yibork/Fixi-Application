from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point

class User(AbstractUser):
    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    is_verified = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    is_service_provider = models.BooleanField(default=False)
    username = models.CharField(max_length=255, unique=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    location = models.PointField(geography=True, default=Point(0.0, 0.0))

    def __str__(self):
        return self.username
