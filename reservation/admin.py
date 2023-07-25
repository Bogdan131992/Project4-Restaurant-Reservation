""" This module contains the admin logic for the booking app. """

from django.contrib import admin
from .models import Reservation, Picture


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    """
    Allows admins a quick overview of all bookings,
    with the ability to filter by date and time for a precise overview.
    intended for use when seating walk-in customers on a given day or
    making business decsions. Also allows for search by booking lead.

    Containts methods to accept or decline the bookings within the dropdown.
    """
    list_display = ('full_name', 'date', 'time', 'guests', 'status',)
    list_filter = ('date', 'time',)
    search_fields = ('full_name',)
    actions = ['accept_reservation', 'decline_reservation']

    def accept_reservation(self, _request, queryset):
        """
        Allows bookings to be accepted from the dropdown menu in admin.
        2 is defined as declined in the STATUS tuple found in models.py on the
        booking directory.
        """
        for reservation in queryset:
            reservation.status = 1
            reservation.save()

    def decline_reservation(self, _request, queryset):
        """
        Allows bookings to be declined from the dropdown menu in admin.
        2 is defined as declined in the STATUS tuple found in models.py on the
        booking directory.
        """
        for reservation in queryset:
            reservation.status = 2
            reservation.save()


@admin.register(Picture)
class PictureAdmin(admin.ModelAdmin):
    """
    The Admin panel for the Image model. found in the booking
    directory under models.py
    """
    list_display = ('name',)