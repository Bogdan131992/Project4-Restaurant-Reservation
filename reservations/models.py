from django.db import models
from django.contrib.auth.models import User

class Table(models.Model):
    name = models.CharField(max_length=50)
    capacity = models.PositiveIntegerField(default=5)

    def __str__(self):
        return self.name

class Reservation(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    guests = models.PositiveIntegerField()

    def __str__(self):
        return f"Reservation ID: {self.id} - {self.user.username} - Table: {self.table.name} - {self.date} at {self.time}"
