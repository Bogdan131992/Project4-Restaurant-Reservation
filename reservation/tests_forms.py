# reservation/tests/test_forms.py

from django.test import TestCase
from .forms import ReservationForm
from .models import Reservation

class ReservationFormTests(TestCase):
    def test_valid_form(self):
        # Test the form with valid data
        data = {
            'full_name': 'John Doe',
            'mobile': '1234567890',
            'date': '2023-07-28',
            'time': '14:00:00',
            'email': 'johndoe@example.com',
            'requests': 'Special requirements',
            'guests': 2,
        }
        form = ReservationForm(data=data)
        if not form.is_valid():
            print(form.errors)
        self.assertTrue(form.is_valid())

    def test_invalid_form_missing_data(self):
        # Test the form with missing data
        data = {}
        form = ReservationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('full_name', form.errors)
        self.assertIn('mobile', form.errors)
        self.assertIn('date', form.errors)
        self.assertIn('time', form.errors)
        self.assertIn('email', form.errors)
        self.assertIn('requests', form.errors)
        self.assertIn('guests', form.errors)

    def test_invalid_form_invalid_guests(self):
        # Test the form with invalid number of guests
        data = {
            'full_name': 'Jane Smith',
            'mobile': '9876543210',
            'date': '2023-07-28',
            'time': '10:00:00',
            'email': 'janesmith@example.com',
            'requests': 'No special requirements',
            'guests': -1,  # Negative number of guests is invalid
        }
        form = ReservationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('guests', form.errors)

