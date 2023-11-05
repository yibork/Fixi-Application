from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db import models
from pictures.models import PictureField
class User(AbstractUser):
    Client = 1
    ServiceProvider = 2
    Admin = 3

    ROLE_CHOICES = (
        (Client, 'Client'),
        (ServiceProvider, 'Service Provider'),
        (Admin, 'Admin'),
    )
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True)
    picture = PictureField(upload_to='users', blank=True, null=True)
    def __str__(self):
        return self.username

