from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Reservation
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class LogInForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['table', 'date', 'time', 'guests']
