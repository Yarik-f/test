# Generated by Django 4.2.16 on 2024-12-14 17:46

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_port_image_port_alter_booking_ship_number_booking'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking_ship',
            name='number_booking',
            field=models.UUIDField(default=uuid.UUID('7c8504cd-f4c4-41ed-9dee-b644a7fad534'), editable=False),
        ),
        migrations.AlterField(
            model_name='routes',
            name='arrival_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='routes',
            name='departure_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
