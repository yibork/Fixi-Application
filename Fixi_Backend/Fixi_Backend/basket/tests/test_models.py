from django.test import TestCase
from django.core.exceptions import ValidationError
from yanvision_ecommerce.promotions.tests.factories import PromoCodeFactory
from yanvision_ecommerce.users.tests.factories import UserFactory
from yanvision_ecommerce.courses.tests.factories import CourseFactory
from yanvision_ecommerce.basket.tests.factories import (
    BasketFactory,
    BasketItemFactory,
    CourseBasketItemFactory,
)


class BasketModelTests(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.basket = BasketFactory(user=self.user)
        self.promo_code = PromoCodeFactory()
        self.course = CourseFactory()

    def test_add_same_product_twice(self):
        self.basket.add_product(self.course)
        self.assertEqual(self.basket.items.count(), 1)

        # Trying to add the same product again should not increase the item count
        self.basket.add_product(self.course)
        self.assertEqual(self.basket.items.count(), 1)

    def test_add_non_existing_product(self):
        with self.assertRaises(ValidationError):
            # Let's simulate adding a non-existing product by passing None
            self.basket.add_product(None)

    def test_apply_used_promo_code(self):
        self.promo_code.quantity = 0  # Set the quantity of the promo code to zero
        self.promo_code.save()
        with self.assertRaises(ValidationError):
            self.basket.apply_promo_code(self.promo_code)


class CourseBasketItemModelTests(TestCase):
    def setUp(self):
        self.basket = BasketFactory(user=UserFactory())
        self.course = CourseFactory()

    def test_save_without_product(self):
        with self.assertRaises(ValidationError):
            # Create a basket item without a product
            # -> Didn't give any product to the basket item
            CourseBasketItemFactory(basket=self.basket, content_object=None)

    def test_save_with_invalid_quantity(self):
        with self.assertRaises(ValidationError):
            # Try saving a basket item with invalid (zero) quantity
            CourseBasketItemFactory(
                basket=self.basket, content_object=self.course, quantity=0
            )

    """
    # Mabghach idouz aslan hit man9edrouch n creyiw basket bla product aslan
    def test_total_price_without_product(self):
        # Didn't give any product to the basket item
        item = CourseBasketItemFactory(
            basket=self.basket, content_object=None, quantity=1
        )
        with self.assertRaises(ValidationError):
            item.total_price()
    """
