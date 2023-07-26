from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('reservation', views.reservation, name='reservation'),

    path('reservations', views.ReservationList.as_view(), name='reservations'),
    path('amend/<reservation_id>/', views.amend_reservation, name='amend'),
    path('booking/', views.booking_view, name='account_booking'),
    path('booking/', views.booking_view, name='booking'),
    path('delete/<int:pk>/', views.delete_reservation, name='delete_reservation'),
    path('login/', views.login_view, name='account_login'),
    path('logout/', views.logout_view, name='account_logout'),
    path('signup/', views.signup_view, name='account_signup'),
    path('cancel/<reservation_id>', views.cancel_reservation, name='cancel'),
]