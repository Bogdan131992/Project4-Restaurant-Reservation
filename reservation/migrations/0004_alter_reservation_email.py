# Generated by Django 3.2.20 on 2023-07-26 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0003_alter_picture_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='email',
            field=models.EmailField(max_length=300),
        ),
    ]
