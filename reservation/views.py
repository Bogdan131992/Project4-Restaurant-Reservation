import datetime
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views import generic
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.http import HttpResponseServerError
from .models import Reservation, Picture
from .forms import ReservationForm
from django.shortcuts import render, redirect, reverse
from .forms import ReservationForm


def index(request):
    try:
        hero = Picture.objects.get(name='hero')
    except ObjectDoesNotExist:
        hero = None
     # Check if the welcome message has been displayed
    if not request.session.get('welcome_message_displayed', False):
        # Set the welcome message to be displayed
        request.session['welcome_message_displayed'] = True
        # Create the message to be displayed
        welcome_message = f"Welcome {request.user.username}"
    else:
        welcome_message = None

    context = {
        'hero': hero,
    }
    return render(request, 'index.html', context)

def reservation(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            reservation_form = ReservationForm(request.POST)

            if reservation_form.is_valid():
                user = request.user
                current_reservation = reservation_form.save(commit=False)
                current_reservation.user = user
                current_reservation.lead = f'{user.first_name} {user.last_name}'
                current_reservation.email = user.email

                try:
                    current_reservation.save()
                except IntegrityError:
                    error = 'You have already requested this reservation'
                    return render(request, 'reservations.html', {
                        "reservation_form": ReservationForm(request.POST),
                        'error': error,
                    })

                return redirect(reverse("reservations"))

            else:
                return render(request, 'reservations.html', {
                    "reservation_form": ReservationForm(request.POST)
                })

        else:
            return render(request, 'reservations.html', {
                "reservation_form": ReservationForm()
            })

    else:
        return redirect(reverse("account_login"))

class ReservationList(generic.ListView):
    model = Reservation

    def sort(self, reservations):
        if reservations.date >= datetime.date.today():
            return True
        else:
            return False

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            reservations = Reservation.objects.filter(user=request.user)
            upcoming_reservations = filter(self.sort, reservations)

            return render(
                request, 'reservations.html',
                {
                    'reservations': upcoming_reservations,
                },
            )

        else:
            return redirect(reverse("account_login"))


def booking_view(request):
    print("Booking View Called")
    booking_form = ReservationForm()
    print(booking_form)
    if request.user.is_authenticated:
        if request.method == 'POST':
            booking_form = ReservationForm(request.POST)
            if booking_form.is_valid():
                # Check if there is any existing reservation with the same date for the same user
                user = request.user
                date = booking_form.cleaned_data['date']
                existing_reservations = Reservation.objects.filter(user=user, date=date)

                if existing_reservations.exists():
                    # Show an alert message informing the user that the date is already booked
                    alert_message = f"A reservation on {date} already exists. Please choose another date."
                    return render(request, 'booking.html', {
                        "booking_form": booking_form,
                        "alert_message": alert_message
                    })
                else:
                    # Save the booking details to the database
                    booking = booking_form.save(commit=False)
                    booking.user = user
                    booking.lead = f'{user.first_name} {user.last_name}'
                    booking.email = user.email
                    booking.save()
                    return redirect(reverse("reservations"))
            else:
                # Form is not valid, render the template with the form and error (if any)
                return render(request, 'booking.html', {
                    "booking_form": booking_form
                })
        else:
            return render(request, 'booking.html', {
                "booking_form": ReservationForm()
            })
    else:
        return redirect(reverse("account_login"))

def cancel_reservation(request, reservation_id):
    if request.user.is_authenticated:
        reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)

        if request.method == 'POST':
            # Process the POST request to cancel the reservation
            reservation.delete()
            return redirect('reservations')

        else:
            return render(request, 'cancel_reservation.html', {
                'reservation': reservation,
            })

    else:
        return redirect('account_login')

def amend_reservation(request, reservation_id):
    if request.user.is_authenticated:
        reservation = get_object_or_404(Reservation, id=reservation_id)
        current_user = request.user

        if current_user == reservation.user:
            context = {
                "mobile": reservation.mobile,
                "date": reservation.date,
                "time": reservation.time,
                "requests": reservation.requests,
                "guests": reservation.guests
            }

            if request.method == 'POST':
                reservation_form = ReservationForm(request.POST, instance=reservation)

                if reservation_form.is_valid():
                    updated_reservation = reservation_form.save(commit=False)
                    updated_reservation.status = 0
                    try:
                        updated_reservation.save()
                    except IntegrityError:
                        error = 'You have already requested this reservation'
                        return render(request, 'amend_reservation.html', {
                            "reservation_form": ReservationForm(request.POST),
                            'error': error,
                        })

                    return redirect(reverse("reservations"))

                else:
                    return render(request, 'amend_reservation.html', {
                        "reservation_form": ReservationForm(request.POST)
                    })

            else:
                reservation_form = ReservationForm(instance=reservation)
                return render(request, 'amend_reservation.html', {
                    "reservation_form": reservation_form,
                    "reservation_id": reservation_id
                })

        else:
            return redirect(reverse("reservations"))

    else:
        return redirect(reverse("account_login"))

@login_required
def delete_reservation(request, reservation_id):
    if request.method == 'POST':
        reservation = get_object_or_404(Reservation, id=reservation_id)
        if request.user == reservation.user:
            reservation.delete()
        return redirect('reservations')

    return HttpResponseServerError("Invalid Request")

@login_required
def error_404(request, exception):
    return render(request, '404.html')

@login_required
def error_500(request):
    return render(request, '500.html')

def login_view(request):
    if request.user.is_authenticated:
        request.session['welcome_message_displayed'] = True
        return redirect('index')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm(request)

    return render(request, 'login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('index')

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()

    return render(request, 'signup.html', {'form': form})