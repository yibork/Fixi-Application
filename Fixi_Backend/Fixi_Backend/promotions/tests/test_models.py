from datetime import timedelta
from django.db import IntegrityError
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from .factories import DiscountFactory, PromoCodeFactory, UserPromoCodeFactory, DiscountForCourseFactory, DiscountForCourseModuleFactory
from yanvision_ecommerce.users.tests.factories import UserFactory
from ..models import PromoCode, Discount, UserPromoCode
from ...courses.tests.factories import CourseFactory, CourseModuleFactory


class DiscountModelTest(TestCase):

    def setUp(self):
        self.course = CourseFactory.create()

    def test_discount_creation(self):
        discount = DiscountForCourseFactory(
            type=Discount.DiscountTypeChoices.PERCENTAGE,
            value=10,
            start_date=timezone.now() - timedelta(days=1),
            end_date=timezone.now() + timedelta(days=1),
            is_active=True,
            content_id=self.course.id,
            content_object=self.course
        )

        self.assertIsInstance(discount, Discount)

    def test_discount_end_date_greater_than_start_date(self):
        with self.assertRaises(ValidationError):
            DiscountForCourseFactory(
                type=Discount.DiscountTypeChoices.PERCENTAGE,
                value=10,
                start_date=timezone.now() + timedelta(days=1),
                end_date=timezone.now() - timedelta(days=1),
                is_active=True,
                content_id=self.course.id,
                content_object=self.course
            )

    def test_discount_invalid_product_type(self):
        with self.assertRaises(ValidationError):
            course_module = CourseModuleFactory()
            DiscountForCourseModuleFactory(
                type=Discount.DiscountTypeChoices.PERCENTAGE,
                value=10,
                start_date=timezone.now() - timedelta(days=1),
                end_date=timezone.now() + timedelta(days=1),
                is_active=True,
                content_id=self.course.id,
                content_object=course_module
            )


class PromoCodeModelTest(TestCase):

    def setUp(self):
        self.user = UserFactory(username='testuser', password='12345')

    def test_promo_code_creation(self):
        promo_code = PromoCodeFactory(
            code='PROMO10',
            type=PromoCode.PromoCodeTypeChoices.PERCENTAGE,
            value=10,
            quantity=5,
            start_date=timezone.now() - timedelta(days=1),
            end_date=timezone.now() + timedelta(days=1),
            created_by=self.user,
            number_of_uses_per_user=3,
            is_active=True,
        )

        self.assertIsInstance(promo_code, PromoCode)

    def test_promo_code_duplicate_code(self):
        with self.assertRaises(IntegrityError):
            PromoCodeFactory(
                code='DUPLICATE_NOT_ALLOWED',
                type=PromoCode.PromoCodeTypeChoices.PERCENTAGE,
                value=10,
                quantity=5,
                start_date=timezone.now() - timedelta(days=1),
                end_date=timezone.now() + timedelta(days=1),
                created_by=self.user,
                number_of_uses_per_user=3,
                is_active=True,
            )
            PromoCodeFactory(
                code='DUPLICATE_NOT_ALLOWED',
                type=PromoCode.PromoCodeTypeChoices.PERCENTAGE,
                value=10,
                quantity=5,
                start_date=timezone.now() - timedelta(days=1),
                end_date=timezone.now() + timedelta(days=1),
                created_by=self.user,
                number_of_uses_per_user=3,
                is_active=True,
            )

    def test_promo_code_end_date_greater_than_start_date(self):
        with self.assertRaises(ValidationError):
            PromoCodeFactory(
                code='PROMO10',
                type=PromoCode.PromoCodeTypeChoices.PERCENTAGE,
                value=10,
                quantity=5,
                start_date=timezone.now() + timedelta(days=1),
                end_date=timezone.now() - timedelta(days=1),
                created_by=self.user,
                number_of_uses_per_user=3,
                is_active=True,
            )


class UserPromoCodeModelTest(TestCase):

    def setUp(self):
        self.user = UserFactory(username='testuser', password='12345')
        self.promo_code = PromoCodeFactory(
            code='PROMO10',
            type=PromoCode.PromoCodeTypeChoices.PERCENTAGE,
            value=10,
            quantity=5,
            start_date=timezone.now() - timedelta(days=1),
            end_date=timezone.now() + timedelta(days=1),
            created_by=self.user,
            number_of_uses_per_user=3,
            is_active=True,
        )

    def test_user_promo_code_creation(self):
        user_promo_code = UserPromoCodeFactory(
            user=self.user,
            promo_code=self.promo_code,
        )

        self.assertIsInstance(user_promo_code, UserPromoCode)

    def test_user_promo_code_unique_constraint(self):
        UserPromoCodeFactory(
            user=self.user,
            promo_code=self.promo_code,
        )

        with self.assertRaises(ValidationError):
            UserPromoCodeFactory(
                user=self.user,
                promo_code=self.promo_code,
            )
