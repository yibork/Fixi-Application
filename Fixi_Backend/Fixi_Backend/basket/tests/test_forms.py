from django.test import TestCase
from yanvision_ecommerce.basket.forms import CheckoutForm


class CheckoutFormTest(TestCase):
    def test_form_valid(self):
        # A form with a valid payment method should be valid.
        form = CheckoutForm({"payment_method": "paypal", "country": "MA"})
        self.assertTrue(form.is_valid())

    def test_form_invalid(self):
        # A form with an invalid payment method should not be valid.
        form = CheckoutForm({"payment_method": "Bitcoin", "country": "MA"})
        self.assertFalse(form.is_valid())

    def test_form_empty(self):
        # A form with no payment method should not be valid.
        form = CheckoutForm({})
        self.assertFalse(form.is_valid())

    def test_form_handles_extra_data(self):
        # A form with extra data should ignore the extra data and still be valid.
        form = CheckoutForm({"payment_method": "paypal","country": "MA", "extra": "data"})
        self.assertTrue(form.is_valid())
        self.assertNotIn("extra", form.cleaned_data)

    def test_form_strip_whitespace(self):
        # The form should not strip leading/trailing whitespace from the payment method.
        # Only CharField Strips the whitespace, we use a ChoiceField
        form = CheckoutForm({"payment_method": " paypal ", "country": "MA"})
        self.assertFalse(form.is_valid())

    def test_form_without_country(self):
        # The form should not strip leading/trailing whitespace from the payment method.
        # Only CharField Strips the whitespace, we use a ChoiceField
        form = CheckoutForm({"payment_method": " paypal "})
        self.assertFalse(form.is_valid())
