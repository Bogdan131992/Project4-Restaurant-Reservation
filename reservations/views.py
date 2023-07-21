# reservations/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, LogInForm, ReservationForm
from .models import Reservation, Table

def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'reservations/sign_up.html', {'form': form})

def log_in(request):
    if request.method == 'POST':
        form = LogInForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('view_tables')
    else:
        form = LogInForm()
    return render(request, 'reservations/log_in.html', {'form': form})

def log_out(request):
    logout(request)
    return redirect('login')

@login_required
def delete_user(request):
    if request.method == 'POST':
        request.user.delete()
        logout(request)
        return redirect('login')
    return render(request, 'reservations/delete_user.html')

@login_required
def view_tables(request):
    tables = Table.objects.all()
    return render(request, 'reservations/view_tables.html', {'tables': tables})

@login_required
def make_reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            if is_table_available(reservation.table, reservation.date, reservation.time):
                reservation.save()
                return redirect('view_reservations')
            else:
                return render(request, 'reservations/table_not_available.html', {'table': reservation.table})
    else:
        form = ReservationForm()
    return render(request, 'reservations/make_reservation.html', {'form': form, 'tables': Table.objects.all()})

@login_required
def view_reservations(request):
    reservations = Reservation.objects.filter(user=request.user)
    return render(request, 'reservations/view_reservations.html', {'reservations': reservations})

@login_required
def edit_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            new_reservation = form.save(commit=False)
            if is_table_available(new_reservation.table, new_reservation.date, new_reservation.time, reservation_id):
                new_reservation.save()
                return redirect('view_reservations')
            else:
                return render(request, 'reservations/table_not_available.html', {'table': new_reservation.table})
    else:
        form = ReservationForm(instance=reservation)
    return render(request, 'reservations/edit_reservation.html', {'form': form, 'tables': Table.objects.all()})

@login_required
def cancel_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    if request.method == 'POST':
        reservation.delete()
        return redirect('view_reservations')
    return render(request, 'reservations/cancel_reservation.html', {'reservation': reservation})

# Helper function to check table availability
def is_table_available(table, date, time, excluded_reservation_id=None):
    reservations = Reservation.objects.filter(table=table, date=date, time=time)
    if excluded_reservation_id:
        reservations = reservations.exclude(id=excluded_reservation_id)
    return reservations.count() < table.capacity
