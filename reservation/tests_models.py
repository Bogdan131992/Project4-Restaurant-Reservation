# reservation/tests/test_models.py

from django.test import TestCase
from django.contrib.auth.models import User
from .models import Reservation

class ReservationModelTests(TestCase):
    def setUp(self):
        # Create a test user
        self.test_user = User.objects.create(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )

    # ...

    def test_unique_constraint(self):
        # Create a Reservation instance
        reservation1 = Reservation.objects.create(
            user=self.test_user,
            full_name='John Doe',
            email='johndoe@example.com',
            mobile='1234567890',
            date='2023-07-28',
            time='10:00:00',
            guests=2,
            requests='Special requirements'
        )

        # Attempt to create another Reservation instance with the same user, date, and time
        with self.assertRaises(Exception):
            reservation2 = Reservation.objects.create(
                user=self.test_user,
                full_name='Jane Smith',
                email='janesmith@example.com',
                mobile='9876543210',
                date='2023-07-28',
                time='10:00:00',
                guests=3,
                requests='No special requirements'
            )

    def test_picture_model_creation(self):
        # Create a Picture instance
        picture = Picture.objects.create(
            picture='path/to/picture.jpg',
            url='https://example.com/path/to/picture.jpg',
            name='Picture 1'
        )

        # Retrieve the picture from the database
        picture_from_db = Picture.objects.get(pk=picture.pk)

        # Check if the values match
        self.assertEqual(picture.picture, 'path/to/picture.jpg')
        self.assertEqual(picture.url, 'https://example.com/path/to/picture.jpg')
        self.assertEqual(picture.name, 'Picture 1')