from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.sign_up, name='sign_up'),
    path('login/', views.log_in, name='login'),
    path('logout/', views.log_out, name='logout'),
    path('delete_user/', views.delete_user, name='delete_user'),
    path('home/', views.view_tables, name='home'),  # Redirect to view_tables after login
    path('view_tables/', views.view_tables, name='view_tables'),
    path('make_reservation/', views.make_reservation, name='make_reservation'),
    path('edit_reservation/<int:reservation_id>/', views.edit_reservation, name='edit_reservation'),
    path('cancel_reservation/<int:reservation_id>/', views.cancel_reservation, name='cancel_reservation'),
    path('view_reservations/', views.view_reservations, name='view_reservations'),
    path('view_all_reservations/', views.view_all_reservations, name='view_all_reservations'),
    path('confirm_reject_reservation/<int:reservation_id>/', views.confirm_reject_reservation, name='confirm_reject_reservation'),
    path('', views.home, name='home'),
]
