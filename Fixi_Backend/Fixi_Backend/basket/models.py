from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from Fixi_Backend.orders.models import Order
from Fixi_Backend.promotions.models import Discount, PromoCode, UserPromoCode
from Fixi_Backend.Catalogue.models import Service

User = get_user_model()

# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    item = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} - {} - {} - {} - {}".format(self.user,
                                               self.item,
                                               self.quantity,
                                               self.created_at,
                                               self.updated_at)


# Basket

class DeliveryCost(models.Model):
    status = models.CharField(max_length=7,
                              choices=(('Active', 'active'), ('Passive', 'passive')),
                              default="passive",
                              null=False)
    cost_per_delivery = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    cost_per_product = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    fixed_cost = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} - {} - {} - {} - {} - {}".format(self.status,
                                                    self.cost_per_delivery,
                                                    self.cost_per_product,
                                                    self.fixed_cost,
                                                    self.created_at,
                                                    self.updated_at)
class Basket(models.Model):
    # user = models.ForeignKey(User, on_delete=moodels.SET_NULL, null=True, related_name='basket', verbose_name=_("User"))
    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="basket",
        verbose_name=_("User"),
    )
    session_key = models.CharField(
        _("Session key"), max_length=40, null=True, blank=True
    )
    promo_code = models.ForeignKey(
        "promotions.PromoCode",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Promo code"),
    )
    # Checkout fields

    # Method called on login
    @staticmethod
    def merge_session_basket_and_user_basket(request):
        user, session_key = request.user, request.session.session_key
        try:
            session_basket = Basket.objects.get(session_key=session_key)
        except Basket.DoesNotExist:
            session_basket = None

        if session_basket:
            try:
                user_basket = Basket.objects.get(user=user)
            except Basket.DoesNotExist:
                user_basket = None

            if user_basket:
                # User already has a basket, so modelsmerge the baskets
                for item in session_basket.items.all():
                    user_basket.add_product(item.item, quantity=item.quantity)
                # Delete the session basket as it's no longer needed
                session_basket.delete()
            else:
                # User doesn't have a basket, so assign the session basket to the user
                session_basket.user = user
                session_basket.save()

    def total_price(self):
        total = 0
        for item in self.items.all():
            total += item.total_price()
        return total

    def add_product(self, service, quantity=1):

        if not service:
            raise ValidationError(_("A service must be provided to add to the basket."))

        # First try to get the object.
        try:
            BasketItem.objects.get(
                basket=self,
                content_type=ContentType.objects.get_for_model(service),
                content_id=service.id,
            )
            # Do nothing in this case the object is already in the basket
            # item.quantity += quantity
            # item.save()

        # If it does not exist, create it.
        except (BasketItem.DoesNotExist, AttributeError): # AttributeError: 'NoneType' object has no attribute '_meta'
            item = BasketItem.objects.create(
                basket=self,
                content_type=ContentType.objects.get_for_model(service),
                content_id=service.id,
            )

    def remove_service(self, service):
        BasketItem.objects.filter(basket=self, item=service).delete()

    def clear_basket(self):
        self.items.all().delete()

    def apply_promo_code(self, promo_code):
        user_promo_code, created = UserPromoCode.objects.get_or_create(
            user=self.user, promo_code=promo_code
        )
        if user_promo_code.usage_count >= promo_code.number_of_uses_per_user:
            raise ValidationError(
                _("You have already used this promo code the maximum times allowed.")
            )
        promo_code_usage_count = (
            Order.objects.all().filter(promo_code=promo_code).count()
        )
        if promo_code.quantity <= promo_code_usage_count:
            raise ValidationError(_("This promo code has been fully redeemed."))
        self.promo_code = promo_code
        self.save()


class BasketItem(models.Model):
    basket = models.ForeignKey(
        "basket.Basket",
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name=_("Basket"),
    )

    service = models.ForeignKey("Catalogue.Service", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(_("Quantity"), default=1)


    def total_price(self):
        return self.service.price * self.quantity
