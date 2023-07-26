import datetime
from django.core.exceptions import ValidationError

def validate_opening_hour(value):
    """
    A custom validation function.
    Intended for use on the time field of the ReservationForm.
    Ensures the input value is between 11 AM and 9 PM.
    If validation is failed, the custom error message is returned.
    """
    if not 11 <= int(value.hour) <= 21:
        raise ValidationError(
            'We only take reservations between 11 AM & 9 PM',
            params={'value': value},
        )

def validate_future_date(value):
    """
    A custom validation function.
    Intended for use on the date field of the ReservationForm.
    Using the datetime method datetime.date.today
    ensures the input value is a future date.
    If validation is failed, the custom error message is returned.

    If value is equal to the current day, provides an alternate error message.
    """
    if value < datetime.date.today():
        raise ValidationError(
            'Please select a future date',
            params={'value': value},
        )
    elif value == datetime.date.today():
        raise ValidationError(
            'Please call to make same-day reservations',
            params={'value': value},
        )

def validate_open_day(value):
    """
    A custom validation function.
    Intended for use on the date field of the ReservationForm.
    Uses the Weekday method of the datetime library.
    Ensures the input value is not a Monday or a Sunday.
    If validation is failed, the custom error message is returned.
    """
    if value.weekday() == 6:
        raise ValidationError(
            'Sunday we are closed, please choose a different date',
            params={'value': value},
        )

def validate_guest_size(value):
    """
    A custom validation function.
    Intended for use on the 'guests' field of the ReservationForm.
    If the input integer is greater than 8,
    validation is failed, and the custom error message is returned.

    Ensures the input integer is also greater than 0.
    """
    if value > 10:
        raise ValidationError(
            'For reservations of more than 10 guests, please call and arrange',
            params={'value': value},
        )
    elif value < 1:
        raise ValidationError(
            'Please let us know how many guests will be attending',
            params={'value': value},
        )
