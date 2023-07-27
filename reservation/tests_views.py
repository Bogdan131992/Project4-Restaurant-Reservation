# reservation/tests_views.py

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Reservation

class ReservationViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.test_user = User.objects.create_user(username='testuser', password='testpassword')

    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_reservation_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('reservation'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reservations.html')

    def test_reservation_view_post(self):
        self.client.login(username='testuser', password='testpassword')
        data = {
            'full_name': 'John Doe',
            'mobile': '1234567890',
            'date': '2023-07-28',
            'time': '14:00:00',
            'email': 'johndoe@example.com',
            'requests': 'Special requirements',
            'guests': 2,
        }
        response = self.client.post(reverse('reservation'), data=data)
        self.assertEqual(response.status_code, 302)  # Expecting a redirect after successful form submission

        # Verify that the reservation was created
        reservation_count = Reservation.objects.filter(user=self.test_user).count()
        self.assertEqual(reservation_count, 1)

    def test_reservations_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('reservations'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reservations.html')

    # Add more test cases for other views as needed
