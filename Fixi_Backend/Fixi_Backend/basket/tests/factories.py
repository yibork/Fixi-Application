from django.contrib.contenttypes.models import ContentType
from factory.django import DjangoModelFactory
from factory import SubFactory, LazyAttribute, SelfAttribute, Iterator
from faker import Faker
from django_countries import countries

from yanvision_ecommerce.users.tests.factories import UserFactory
from yanvision_ecommerce.courses.tests.factories import CourseFactory
from yanvision_ecommerce.promotions.tests.factories import PromoCodeFactory
from ..models import Basket, BasketItem

faker = Faker()


class BasketFactory(DjangoModelFactory):
    class Meta:
        model = Basket

    user = SubFactory(UserFactory)
    session_key = LazyAttribute(lambda x: faker.uuid4())
    promo_code = SubFactory(PromoCodeFactory)
    country = Iterator(countries)


"""
class BasketItemFactory(DjangoModelFactory):
    content_id = SelfAttribute('content_object.id')
    content_type = LazyAttribute(lambda o: ContentType.objects.get_for_model(o.content_object))

    class Meta:
        model = BasketItem
        exclude = ['content_object']

    basket = SubFactory(BasketFactory)
    quantity = LazyAttribute(lambda x: faker.random_int(min=1, max=5))
"""


class BasketItemFactory(DjangoModelFactory):
    content_id = LazyAttribute(
        lambda o: o.content_object.id if o.content_object else None
    )
    content_type = LazyAttribute(
        lambda o: ContentType.objects.get_for_model(o.content_object)
        if o.content_object
        else None
    )

    class Meta:
        model = BasketItem
        exclude = ["content_object"]

    basket = SubFactory(BasketFactory)
    quantity = LazyAttribute(lambda x: faker.random_int(min=1, max=5))


class CourseBasketItemFactory(BasketItemFactory):
    content_object = SubFactory(CourseFactory)
