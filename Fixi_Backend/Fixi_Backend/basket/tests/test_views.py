from django.test import TestCase, Client
from django.urls import reverse
from django.core.exceptions import ValidationError
from yanvision_ecommerce.users.tests.factories import UserFactory
from yanvision_ecommerce.promotions.tests.factories import PromoCodeFactory
from yanvision_ecommerce.courses.tests.factories import CourseFactory
from yanvision_ecommerce.basket.tests.factories import BasketFactory, CourseBasketItemFactory


class BasketViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserFactory()
        self.promo_code = PromoCodeFactory()
        self.course = CourseFactory()
        self.basket = BasketFactory(user=self.user)
        self.basket_item = CourseBasketItemFactory(basket=self.basket, content_object=self.course)
        self.client.force_login(self.user)

    def test_apply_nonexistent_promo_code(self):
        response = self.client.post(reverse('basket:apply-promo-code'), {'promo_code': 'NONEXISTENT'})
        self.assertEqual(response.status_code, 400)

    def test_add_nonexistent_product_to_basket(self):
        response = self.client.post(reverse('basket:add-item'), {'product_type': 'course', 'product_id': '999'})
        self.assertEqual(response.status_code, 404)

    def test_remove_nonexistent_product_from_basket(self):
        with self.assertRaises(ValidationError):
            response = self.client.post(reverse('basket:remove-item'), {'product_type': 'course', 'product_id': '999'})
            self.assertEqual(response.status_code, 400)

    def test_clear_empty_basket(self):
        self.basket.clear_basket()
        response = self.client.post(reverse('basket:clear-basket'))
        self.assertEqual(response.status_code, 200)  # Should not raise error even if basket is empty

    def test_checkout_empty_basket(self):
        self.basket.clear_basket()
        response = self.client.post(reverse('basket:checkout'), {'country': 'MA'})
        self.assertEqual(response.status_code, 400)  # Should raise an error when trying to checkout empty basket

    def test_checkout_nonempty_basket_without_country(self):
        # Trying to checkout without providing a country should raise an error
        response = self.client.post(reverse('basket:checkout'), {})
        self.assertEqual(response.status_code, 400)
