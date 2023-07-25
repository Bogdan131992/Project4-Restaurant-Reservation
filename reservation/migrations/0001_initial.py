# Generated by Django 3.2.20 on 2023-07-25 10:06

import cloudinary.models
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picrure', cloudinary.models.CloudinaryField(max_length=255, verbose_name='picture')),
                ('url', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=80)),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=300)),
                ('email', models.CharField(max_length=300)),
                ('mobile', models.CharField(max_length=15, validators=[django.core.validators.RegexValidator(regex='^\\+?1?\\d{9,15}$')])),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('guests', models.PositiveIntegerField()),
                ('requests', models.TextField(max_length=400)),
                ('status', models.IntegerField(choices=[(0, 'pending'), (1, 'accepted'), (2, 'declined')], default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.AddConstraint(
            model_name='reservation',
            constraint=models.UniqueConstraint(fields=('user', 'date', 'time'), name='unique_booking'),
        ),
    ]