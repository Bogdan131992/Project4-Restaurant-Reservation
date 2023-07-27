
from django.test import TestCase
from reservation.forms import ReservationForm
from reservation.models import Reservation
from django.utils import timezone

class ReservationFormTests(TestCase):
    def test_valid_form(self):
        # Create test data
        data = {
            'full_name': 'John Doe',
            'mobile': '1234567890',
            'date': timezone.now().date(),
            'time': timezone.now().time(),
            'email': 'johndoe@example.com',
            'requests': 'Test special requirements',
            'guests': 4,
        }

        # Create the form instance with test data
        form = ReservationForm(data=data)

        # Check if the form is valid
        self.assertTrue(form.is_valid())

    # def test_invalid_form(self):
    #     # Create test data with invalid inputs (e.g., empty fields)
    #     data = {
    #         'full_name': '',
    #         'mobile': '',
    #         'date': '',
    #         'time': '',
    #         'email': 'invalid-email',
    #         'requests': 'a' * 301,  # Exceeding max_length
    #         'guests': -1,           # Invalid number of guests
    #     }

        # Create the form instance with test data
        form = ReservationForm(data=data)

        # Check if the form is invalid
        self.assertFalse(form.is_valid())

    def test_future_date_validation(self):
        # Create test data with a past date
        data = {
            'full_name': 'John Doe',
            'mobile': '1234567890',
            'date': timezone.now().date() - timezone.timedelta(days=1),
            'time': timezone.now().time(),
            'email': 'johndoe@example.com',
            'requests': 'Test special requirements',
            'guests': 4,
        }

        # Create the form instance with test data
        form = ReservationForm(data=data)

        # Check if the date validation fails
        self.assertFalse(form.is_valid())
        self.assertIn('date', form.errors)

    

