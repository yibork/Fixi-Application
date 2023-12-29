from django.db import models
from pictures.models import PictureField
from treebeard.mp_tree import MP_Node
from django.utils.text import slugify
from Fixi_Backend.base import AbstractBaseModel

class Service(AbstractBaseModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=750, unique=True, null=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    image = PictureField(upload_to='service', blank=True)
    created_by = models.ForeignKey('users.User', on_delete=models.CASCADE,null=True, blank=True)
    #discount = models.ForeignKey('Discount', on_delete=models.CASCADE, null=True, blank=True)
    taxonomies = models.ManyToManyField('Taxonomy', through='ServiceTaxonomy', related_name='services')
    def __str__(self):
        return self.name
class Taxonomy(MP_Node, AbstractBaseModel):
    name = models.CharField(max_length=100)
    node_order_by = ['name']
    slug = models.SlugField(max_length=750, unique=True, null=True)
    #discount = models.ForeignKey('Discount', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id and not self.slug:  # Check if it's a new object
            self.slug = self._generate_unique_slug(self.name)

        super().save(*args, **kwargs)

    def _generate_unique_slug(self, name):
        slug = slugify(name)
        unique_slug = slug
        suffix = 1

        while Service.filter(slug=unique_slug).exists():
            unique_slug = f"{slug}-{suffix}"
            suffix += 1

        return unique_slug

    def get_parent(self, update=False):
        return super().get_parent(update)


class ServiceTaxonomy(AbstractBaseModel):
    taxonomy = models.ForeignKey('Taxonomy', on_delete=models.CASCADE)
    service = models.ForeignKey('Service', on_delete=models.CASCADE)

class FixiService(AbstractBaseModel):
    service = models.ForeignKey('Service', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    client = models.ForeignKey('users.User', on_delete=models.CASCADE,null=True, blank=True,limit_choices_to={'role': 1})
    service_provider = models.ForeignKey('users.User', on_delete=models.CASCADE,null=True, blank=True, related_name='service_provider',limit_choices_to={'role': 2})
    time = models.DateTimeField(null=True, blank=True)
    # Service Status Choices
    PENDING = 'pending'
    CONFIRMED = 'confirmed'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (CONFIRMED, 'Confirmed'),
        (IN_PROGRESS, 'In Progress'),
        (COMPLETED, 'Completed'),
        (CANCELLED, 'Cancelled'),
    ]

    status = models.CharField(
        max_length=100,
        choices=STATUS_CHOICES,
        default=PENDING,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.service.name