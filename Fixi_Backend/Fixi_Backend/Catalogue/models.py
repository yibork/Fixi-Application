from django.db import models
from pictures.models import PictureField
class Catalogue(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    image = PictureField(upload_to='catalogue', blank=True)
    created_by = models.ForeignKey('users.User', on_delete=models.CASCADE,null=True, blank=True)
    image_width = models.PositiveIntegerField(null=True, blank=True)
    image_height = models.PositiveIntegerField(null=True, blank=True)
