def is_table_available(table, date, time, excluded_reservation_id=None):
    reservations = Reservation.objects.filter(table=table, date=date, time=time)
    if excluded_reservation_id:
        reservations = reservations.exclude(id=excluded_reservation_id)
    return reservations.count() < table.capacity
