from django import forms
from django.utils.translation import gettext_lazy as _

from django_countries.fields import CountryField


class CheckoutForm(forms.Form):
    CHOICES = [
        ("paypal", "PayPal (Fake)"),
        ("stripe", "Stripe (Fake)"),
    ]

    payment_method = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, required=True)
    country = CountryField(
        blank_label=_("(Select country)"),
    ).formfield(required=True)
