from django import forms
from django.utils.translation import gettext_lazy as _
from .models import PromoCode, UserPromoCode


class UserPromoCodeForm(forms.Form):
    promo_code = forms.CharField(
        max_length=100,
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

    def clean_promo_code(self):
        promo_code_str = self.cleaned_data.get("promo_code")

        try:
            promo_code = PromoCode.active_promo_codes_objects.get(code=promo_code_str)
        except PromoCode.DoesNotExist as ex:
            raise forms.ValidationError(_("The entered Promo Code is invalid.")) from ex

        # Check if the promo code is already added by the user
        user_promo_code = UserPromoCode.objects.filter(user=self.user, promo_code=promo_code).first()

        if user_promo_code:
            raise forms.ValidationError(_("You have already added this Promo Code."))

        # Check if the promo code is valid for the user
        is_valid, message = promo_code.is_valid_for_user(self.user)

        if not is_valid:
            raise forms.ValidationError(message)

        return promo_code
