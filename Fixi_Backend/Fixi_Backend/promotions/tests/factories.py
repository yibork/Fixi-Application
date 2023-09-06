from datetime import timedelta
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from factory.django import DjangoModelFactory
from factory import SubFactory, Faker, SelfAttribute, LazyAttribute
from factory.fuzzy import FuzzyInteger, FuzzyDecimal, FuzzyChoice

from ..models import Discount, PromoCode, UserPromoCode


class DiscountFactory(DjangoModelFactory):
    type = FuzzyChoice(Discount.DiscountTypeChoices.choices)
    value = FuzzyDecimal(0, 1000, 2)
    start_date =timezone.now() - timedelta(days=1)
    end_date = timezone.now() + timedelta(days=1)
    is_active = Faker("boolean")
    content_id = SelfAttribute("content_object.id")
    content_type = LazyAttribute(
        lambda o: ContentType.objects.get_for_model(o.content_object)
    )

    class Meta:
        model = Discount
        exclude = ["content_object"]
        abstract = True


class DiscountForCourseFactory(DiscountFactory):
    content_object = SubFactory("courses.tests.factories.CourseFactory")

    class Meta:
        model = Discount


# False factory to only test assertFalse
class DiscountForCourseModuleFactory(DiscountFactory):
    content_object = SubFactory("courses.tests.factories.CourseModuleFactory")

    class Meta:
        model = Discount


class PromoCodeFactory(DjangoModelFactory):
    class Meta:
        model = PromoCode

    code = Faker("pystr", max_chars=100)
    type = FuzzyChoice(PromoCode.PromoCodeTypeChoices.choices)
    value = FuzzyDecimal(0, 1000, 2)
    quantity = FuzzyInteger(1, 1000)
    start_date =timezone.now() - timedelta(days=1)
    end_date = timezone.now() + timedelta(days=1)
    created_by = SubFactory("users.tests.factories.UserFactory")
    number_of_uses_per_user = FuzzyInteger(1, 10)
    is_active = Faker("boolean")


class UserPromoCodeFactory(DjangoModelFactory):
    class Meta:
        model = UserPromoCode

    user = SubFactory("users.tests.factories.UserFactory")
    promo_code = SubFactory(PromoCodeFactory)
