""" This module contains the form logic for making a booking. """

from django import forms
from .models import Reservation
from .widget import DatePickerInput, TimePickerInput
from . import validators


class ReservationForm(forms.ModelForm):
    """
    Creates the BookingForm class that inherits from Django' base form.
    Provides the labels and placeholder text for each field.
    Provides the widgets and handles validation where required.
    The custom validator logic can be found in the booking directory
    in validators.py.
    """

    mobile = forms.CharField(
        label='Contact Number',
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Mobile'}),
    )

    date = forms.DateField(
        label='Date of Booking',
        required=True,
        widget=DatePickerInput(),
        validators=[
            validators.validate_future_date, validators.validate_open_day
            ],
    )

    time = forms.TimeField(
        label='Arrival Time',
        required=True,
        widget=TimePickerInput(),
        validators=[validators.validate_opening_hour],
    )

    notes = forms.CharField(
        label='Special Requirements',
        required=False,
        widget=forms.Textarea(attrs={
            'placeholder': 'Any special requirements we should be aware of?'
        }),
        max_length=300,
    )

    guests = forms.IntegerField(
        label='Number of Guests',
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Guests'}),
        validators=[validators.validate_guest_size],
    )

    class Meta:
        """
        The booking form inherits from the Booking model.
        Takes the required fields needed for a user to make a new booking.

        Defines the widgets for the date and time fields.
        """
        model = Reservation

        fields = (
            'mobile', 'date', 'time', 'notes', 'guests'
        )

        widgets = {
            'date': DatePickerInput,
            'time': TimePickerInput,
        }