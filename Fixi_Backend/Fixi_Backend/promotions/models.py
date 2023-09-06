from django.utils import timezone
from django.apps import apps
from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model


from Fixi_Backend.core.models import AbstractBaseModel


User = get_user_model()

# Create your models here.


class ActiveDiscountManager(models.Manager):
    def get_queryset(self):
        now = timezone.now()
        return (
            super()
            .get_queryset()
            .filter(
                is_active=True,
                start_date__lte=now,
                end_date__gte=now,
            )
        )


class Discount(models.Model):
    objects = models.Manager()
    active_discounts = ActiveDiscountManager()

    class DiscountTypeChoices(models.TextChoices):
        PERCENTAGE = "percentage", _("Percentage")
        AMOUNT = "amount", _("Amount")

    type = models.CharField(max_length=100, choices=DiscountTypeChoices.choices)
    value = models.DecimalField(
        _("Value"),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    start_date = models.DateTimeField(_("Start date"))
    end_date = models.DateTimeField(_("End date"))
    is_active = models.BooleanField(_("Is active"), default=False)

    # Product
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    content_id = models.PositiveIntegerField()
    product = GenericForeignKey("content_type", "content_id")

    def __str__(self):
        return str(self.value)

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def clean(self):
        super().clean()

        # Check that the content object is a Course or Webinar
        valid_content_types = []

        for product_model in settings.PRODUCT_MODELS:
            app_label, model_name = product_model.split(".")
            content_type = ContentType.objects.get(
                app_label=app_label, model=model_name.lower()
            )
            valid_content_types.append(content_type)

        if self.content_type not in valid_content_types:
            raise ValidationError(
                "Invalid product type. Please select a Course or a Webinar."
            )

        # make sure end date is later than start date
        if self.start_date and self.end_date:
            if self.end_date <= self.start_date:
                raise ValidationError(_("End date must be later than start date"))

        # make sure that the value is positive and if user choose percentage type the value must be lte 100
        if self.type == self.DiscountTypeChoices.PERCENTAGE:
            validators = [
                MinValueValidator(0),
                MaxValueValidator(100),
            ]
            for validator in validators:
                validator(self.value)
        else:
            validators = [
                MinValueValidator(0),
            ]
            for validator in validators:
                validator(self.value)


class ActivePromoCodeManager(models.Manager):
    def get_queryset(self):
        now = timezone.now()
        return (
            super()
            .get_queryset()
            .filter(
                is_active=True,
                start_date__lte=now,
                end_date__gte=now,
            )
        )


class PromoCode(models.Model):
    objects = models.Manager()
    active_promo_codes_objects = ActivePromoCodeManager()

    class PromoCodeTypeChoices(models.TextChoices):
        PERCENTAGE = "percentage", _("Percentage")
        AMOUNT = "amount", _("Amount")

    code = models.CharField(_("Code"), max_length=100, unique=True)
    type = models.CharField(
        _("Type"), max_length=100, choices=PromoCodeTypeChoices.choices
    )
    value = models.DecimalField(
        _("Value"),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    quantity = models.PositiveIntegerField(_("Quantity"), default=1)
    start_date = models.DateTimeField(_("Start date"))
    end_date = models.DateTimeField(_("End date"))
    created_by = models.ForeignKey(
        User,
        verbose_name=_("Created by"),
        related_name="created_promocodes",
        on_delete=models.CASCADE,
    )
    # Set days until the promo code is removed from the promo code basket if not used
    days_until_expired_by_user = models.PositiveIntegerField(default=0)
    number_of_uses_per_user = models.PositiveIntegerField(
        _("Number of uses per user"), default=1
    )
    is_active = models.BooleanField(_("Is active"), default=False)

    def __str__(self):
        return self.code

    def clean(self):
        super().clean()

        # make sure end date is later than start date
        if self.start_date and self.end_date:
            if self.end_date <= self.start_date:
                raise ValidationError(_("End date must be later than start date"))

        # make sure that the value is positive and if user choose percentage type the value must be lte 100
        if self.type == self.PromoCodeTypeChoices.PERCENTAGE:
            validators = [
                MinValueValidator(0),
                MaxValueValidator(100),
            ]
            for validator in validators:
                validator(self.value)
        else:
            validators = [
                MinValueValidator(0),
            ]
            for validator in validators:
                validator(self.value)

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    @property
    # Number of times this promo code is used in Pending or Paid Orders
    def usage_count(self):
        Order = apps.get_model("orders", "Order")
        return Order.objects.filter(promo_code=self).count()

    def is_valid_for_user(self, user):
        # Check if the promo code is already added by the user
        user_promo_code = UserPromoCode.objects.filter(
            user=user, promo_code=self
        ).first()

        if user_promo_code and user_promo_code.remaining_usage_count <= 0:
            return False, _(
                "You have already used this Promo Code the maximum times allowed."
            )

        # Check if the promo code has been used up
        if self.quantity <= self.usage_count:
            return False, _("This Promo Code has been fully redeemed.")

        return True, ""


class UserPromoCode(AbstractBaseModel):
    user = models.ForeignKey(
        User,
        related_name="user_promo_codes",
        on_delete=models.CASCADE,
        verbose_name=_("User"),
    )
    promo_code = models.ForeignKey(
        PromoCode,
        related_name="user_promo_codes",
        on_delete=models.CASCADE,
        verbose_name=_("Promo code"),
    )

    class Meta:
        unique_together = (
            "user",
            "promo_code",
        )

    def __str__(self):
        return f"{self.user} - {self.promo_code}"

    def clean(self) -> None:
        super().clean()

        # Check if a UserPromoCode with the given user and promo code already exists
        exists = UserPromoCode.objects.filter(
            user=self.user, promo_code=self.promo_code
        ).exists()
        if exists:
            raise ValidationError(
                "A UserPromoCode with this user and promo code already exists."
            )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    @property
    # TODO: Number of times this user used this promo code in his Pending or Paid Orders
    def usage_count(self):
        Order = apps.get_model("orders", "Order")
        return Order.objects.filter(user=self.user, promo_code=self.promo_code).count()

    @property
    def remaining_usage_count(self):
        # Total number of times the promo code has been used by all users
        global_usage_count = self.promo_code.usage_count
        # Remaining number of times this user can use this promo code
        user_remaining_usage = (
            self.promo_code.number_of_uses_per_user - self.usage_count
        )
        # Remaining number of times the promo code can be used in total
        global_remaining_usage = self.promo_code.quantity - global_usage_count
        return min(user_remaining_usage, global_remaining_usage)
