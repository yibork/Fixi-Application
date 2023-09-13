from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Basket(models.Model):
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

    # Add service field directly to the Basket model


    # Add other fields relevant to your Basket model here

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
                # User already has a basket, so merge the items from the session basket
                user_basket.service = session_basket.service
                user_basket.save()
                # Delete the session basket as it's no longer needed
                session_basket.delete()
            else:
                # User doesn't have a basket, so assign the session basket to the user
                session_basket.user = user
                session_basket.save()

    def total_price(self):
        return self.service.price
