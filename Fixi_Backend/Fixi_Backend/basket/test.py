from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from .models import Basket  # Import your Basket model
from ..Catalogue.models import Service  # Import your Service model

User = get_user_model()

class BasketAPITestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()
        self.client.login(username='testuser', password='testpass')
        self.service = Service.objects.create(name='Test Service', price=10)

    def test_add_service_to_basket_authenticated(self):
        url = '/add_service_to_basket/'
        data = {'service_id': self.service.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Basket.objects.filter(user=self.user).count(), 1)

    def test_add_service_to_basket_unauthenticated(self):
        self.client.logout()  # Log out the user
        url = '/add_service_to_basket/'
        data = {'service_id': self.service.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Basket.objects.filter(session_key=self.client.session.session_key).count(), 1)
