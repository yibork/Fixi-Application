from django.test import TestCase
from django.utils.translation import gettext_lazy as _
from datetime import timedelta
from django.utils import timezone
from yanvision_ecommerce.courses.tests.factories import CoursesFactory
from ..forms import UserPromoCodeForm
from .factories import PromoCodeFactory, UserPromoCodeFactory, DiscountFactory
from yanvision_ecommerce.users.tests.factories import UserFactory
from faker import Faker

from ..models import Discount, PromoCode

fake = Faker()

class UserPromoCodeFormTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory(username='TestUser', password='TestPassword')
        start_date = timezone.now()
        end_date = start_date + timedelta(days=30)  # ensure end_date is later than start_date

        self.valid_promo_code = PromoCodeFactory.create(
            code='TestCodeValid',
            type=PromoCode.PromoCodeTypeChoices.AMOUNT,
            value=10,
            quantity=5,
            start_date=start_date,
            end_date=end_date,
            is_active=True,
            created_by=self.user,
            number_of_uses_per_user=1
        )

        self.promo_code = PromoCodeFactory.create(
            code='TestCode',
            type=PromoCode.PromoCodeTypeChoices.AMOUNT,
            value=10,
            quantity=5,
            start_date=start_date,
            end_date=end_date,
            is_active=True,
            created_by=self.user,
            number_of_uses_per_user=1
        )

    def test_form_invalid_promo_code(self):
        form = UserPromoCodeForm(data={'promo_code': 'NonExistentCode'}, user=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn('promo_code', form.errors)
        self.assertEqual(form.errors['promo_code'][0], _("The entered Promo Code is invalid."))

    def test_form_promo_code_already_added(self):
        UserPromoCodeFactory.create(user=self.user, promo_code=self.promo_code)
        form = UserPromoCodeForm(data={'promo_code': self.promo_code.code}, user=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn('promo_code', form.errors)
        self.assertEqual(form.errors['promo_code'][0], _("You have already added this Promo Code."))

    def test_form_promo_code_not_valid_for_user(self):
        self.promo_code.quantity = 0
        self.promo_code.save()
        form = UserPromoCodeForm(data={'promo_code': self.promo_code.code}, user=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn('promo_code', form.errors)
        self.assertEqual(form.errors['promo_code'][0], _("This Promo Code has been fully redeemed."))

    def test_form_valid(self):
        form = UserPromoCodeForm(data={'promo_code': self.valid_promo_code.code}, user=self.user)
        form.is_valid()
        self.assertTrue(form.is_valid())
        print(form.errors)
        self.assertEqual(form.cleaned_data.get('promo_code'), self.valid_promo_code)
