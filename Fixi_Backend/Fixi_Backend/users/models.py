from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    is_verified = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    is_service_provider = models.BooleanField(default=False)
    username = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.username
    def has_purchased_product(self, product):
        # Implement the logic for checking if a user has purchased a product
        pass

    def has_reviewed_product(self, product):
        # Implement the logic for checking if a user has reviewed a product
        pass

class Address(models.Model):
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return self.address
