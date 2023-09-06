from factory.django import DjangoModelFactory
from factory import LazyAttribute, SubFactory, post_generation
from faker import Faker
from django.contrib.contenttypes.models import ContentType
from yanvision_ecommerce.promotions.tests.factories import PromoCodeFactory
from yanvision_ecommerce.users.tests.factories import UserFactory

from ..models import Order, OrderItem

fake = Faker()


class OrderFactory(DjangoModelFactory):
    class Meta:
        model = Order

    order_number = LazyAttribute(lambda x: Order.generate_order_number())
    user = SubFactory(UserFactory)
    promo_code = SubFactory(PromoCodeFactory)
    payment_method = LazyAttribute(lambda x: fake.random_element(Order.PaymentMethodChoices.choices)[0])
    status = LazyAttribute(lambda x: fake.random_element(Order.OrderStatusChoices.choices)[0])
    total_amount = LazyAttribute(lambda x: fake.pydecimal(right_digits=2, positive=True, min_value=20, max_value=100))
    billing_address = LazyAttribute(lambda x: fake.address())
    billing_country = LazyAttribute(lambda x: fake.country_code())
    paid_at = None

    @post_generation
    def mark_paid_for_user(self, create, extracted, **kwargs):
        if extracted:
            self.mark_paid_for_user()


class OrderItemFactory(DjangoModelFactory):
    class Meta:
        model = OrderItem

    order = SubFactory(OrderFactory)
    content_type = LazyAttribute(lambda x: ContentType.objects.order_by('?').first())
    content_id = LazyAttribute(lambda x: fake.random_int(min=1, max=100))
    quantity = LazyAttribute(lambda x: fake.random_int(min=1, max=5))
    price = LazyAttribute(lambda x: fake.pydecimal(right_digits=2, positive=True, min_value=20, max_value=100))

    @post_generation
    def item(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            self.item = extracted
        else:
            self.item = None
