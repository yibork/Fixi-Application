from django.contrib.auth.models import AbstractUser
from django.apps import apps
from django.db.models import CharField, BooleanField, ForeignKey, ManyToManyField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from django.db import models

from Fixi_Backend.core.models import AbstractBaseModel


class User(AbstractUser):
    """
    Default custom user model for Fixi_Backend.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    #: First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = CharField(max_length=150, blank=True, verbose_name="first name")
    last_name = CharField(max_length=150, blank=True, verbose_name="last name")

    is_verified = BooleanField(default=False)
    verify_token = CharField(max_length=20, null=True, blank=True)
    phone_number = CharField(max_length=20, null=True, blank=True)
    
    def get_absolute_url(self):
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})
    
    def has_purchased_product(self, product):
        Order = apps.get_model('orders', 'Order')
        return Order.objects.filter(order_items__product=product, user=self).exists()
    
    def has_reviewed_product(self, product):
        Review = apps.get_model('orders', 'Review')
        return Review.objects.filter(product=product, user=self).exists()


class Address(AbstractBaseModel):
    address = CharField(max_length=255)
    city = CharField(max_length=100)
    is_primary = BooleanField()
    postal_code = CharField(max_length=20)
    user = ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.address

User.groups.related_name = 'auth_user_groups'

