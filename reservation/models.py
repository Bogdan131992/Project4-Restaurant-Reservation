from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from cloudinary.models import CloudinaryField


# A tuple to hold the status key for the Reservation model.
STATUS = ((0, "pending"), (1, "accepted"), (2, "declined"))


class Reservation(models.Model):
    """
    Model representing individual reservations made in the booking app.

    Inherits the user from account sign-up.
    Stores booking details: full_name, email, mobile, date, time,
    and number of guests for each reservation, along with any special requirements.

    Default booking status is 'pending' using the above tuple.

    Mobile field validation is handled with Django's inbuilt RegexValidator.
    """
    # Foreign Key from the User model
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # User Info needed for Booking
    full_name = models.CharField(max_length=300, blank=False)
    email = models.EmailField(max_length=300, blank=False)
    # Contact Number for Booking & Validator
    phoneNumberRegex = RegexValidator(regex=r'^\+?1?\d{9,15}$')
    mobile = models.CharField(validators=[phoneNumberRegex], max_length=15, blank=False)
    # Date of Booking
    date = models.DateField(blank=False)
    # Time of Booking
    time = models.TimeField(blank=False)
    # Number of Guests on Booking
    guests = models.PositiveIntegerField(blank=False)
    # Special Requests for Booking
    requests = models.TextField(max_length=400, blank=False)
    # Booking Status - status updates handled in admin
    status = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        """
        Model metadata for the Reservation model.

        Orders reservations by date in descending order.

        Uses Django's inbuilt UniqueConstraint method to ensure
        a user cannot make a duplicate reservation for the same
        date & time as one they already have stored in the Reservation database.

        If a double reservation is attempted, the error is handled in the
        relevant views in the booking directory (views.py).
        """
        ordering = ['-date']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'date', 'time'], name='unique_reservation'
            ),
        ]

    def __str__(self):
        """
        Returns a string representation of the reservation.

        The booking date and time are used as the reservation title.
        Defining this method is recommended by Django.
        """
        return f'{self.date} {self.time}'


class Picture(models.Model):
    """
    Model representing images used in the restobook project.

    Stores the image using CloudinaryField for ease of coding.
    Also allows admins to store the URL of where the image is hosted
    on Cloudinary.
    """
    picture = CloudinaryField('picture')
    url = models.CharField(max_length=300)
    name = models.CharField(max_length=80, blank=False)
