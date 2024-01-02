from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db import models
from pictures.models import PictureField
from django.conf import settings
from django.core.validators import MaxValueValidator
from django.contrib.gis.db import models as gis_models

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
    taxonomy = models.ForeignKey(
        'Catalogue.Taxonomy',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='service_providers'
    )
    location = gis_models.PointField(geography=True, null=True, blank=True)


    def __str__(self):
        return self.username

class Review(models.Model):
    # Assuming there's a model for Service. If not, you might want to link directly to the User model.
    service_provider = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='reviews', limit_choices_to={'role': User.ServiceProvider})
    client = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='client_reviews', limit_choices_to={'role': User.Client})
    service = models.ForeignKey('Catalogue.FixiService', on_delete=models.CASCADE, related_name='reviews')  # Replace 'YourServiceModel' with your actual service model

    rating = models.PositiveSmallIntegerField(validators=[MaxValueValidator(5)])
    comment = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review by {self.client.username} on {self.service_provider.username}"
